from urllib.parse import urljoin, urlparse
from scrapers.Scraper import Scraper

import time

from db.database import database_instance

class LinkScraper(Scraper):

    """
    A class used to represent an link scraper that processes
    the page and extracts the link,
    then sends a task for asynchronous processing
    """

    def __init__(self, link):       
        super().__init__(link)
        self.links = self.get_links_from_html()
        self.send_links_to_db()

    def get_links_from_html(self):
        changed_links = []

        if self.soup is None:
            return changed_links

        # Get links from <a> tags
        links = [a["href"] for a in self.soup.find_all("a", href=True)]

        # Take only unique links
        temp_links = set(links)
        links = list(temp_links)

        print(links)

        # Get domain of the page
        self.domain = urlparse(self.link).netloc

        # Handle relative links
        for link in links:
            if link.startswith("#") or link.startswith("?"):
                continue
            if link.startswith("/"):
                changed_link = urljoin(self.link, link)
                if urlparse(changed_link).netloc == self.domain:
                    changed_links.append(changed_link)
            elif urlparse(link).netloc == self.domain:
                changed_links.append(link)

        return changed_links

    def is_link_unique(self, link):
        #Check if a link already exists in the Firestore database. Return False or True
        docs = database_instance.db.collection('news').where('url', '==', link).get()
        return len(docs) == 0

    def send_links_to_db(self):
        current_time = time.localtime()

        # Форматирование времени в строку в формате "DD.MM.YYYY"
        formatted_date = time.strftime("%d.%m.%Y", current_time)

        batch = database_instance.db.batch()

        licznik = 0

        for link in self.links:
            if self.is_link_unique(link):
                doc_ref = database_instance.db.collection('news').document()

                licznik += 1

                data = {
                    "id": doc_ref.id,
                    "url": link,
                    "tags": [],
                    "date": formatted_date,
                    "domain": self.domain,
                }

                batch.set(doc_ref, data)

        print(f"Were pushed links to DB: {licznik}")
        batch.commit()