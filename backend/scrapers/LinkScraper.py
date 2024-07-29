import time
from urllib.parse import urljoin, urlparse
from scrapers.Scraper import Scraper
from db.database import database_instance


class LinkScraper(Scraper):
    """
    A class used to represent a link scraper
    that processes the page and extracts the links
    """
    def __init__(self, link):       
        super().__init__(link)
        self.links = self.get_links_from_html()
        self.send_links_to_db()

    def get_links_from_html(self):
        """
        Get links from an HTML file
        """
        changed_links = []

        if self.soup is None:
            return changed_links

        # Get links from <a> tags
        links = [a["href"] for a in self.soup.find_all("a", href=True)]

        # Take only unique links
        temp_links = set(links)
        links = list(temp_links)

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
        """
        Check if a link already exists in the Firestore database.
        
        Return False or True
        """
        docs = database_instance.db.collection('news').where('url', '==', link).get()
        return len(docs) == 0

    def send_links_to_db(self):
        """
        Send links to DB
        """
        # Get the current time
        current_time = time.localtime()

        # Format the string as "DD.MM.YYYY"
        formatted_date = time.strftime("%d.%m.%Y", current_time)

        batch = database_instance.db.batch()
        counter = 0

        for link in self.links:
            if self.is_link_unique(link):
                doc_ref = database_instance.db.collection('news').document()

                counter += 1

                data = {
                    "id": doc_ref.id,
                    "url": link,
                    "tags": [],
                    "date": formatted_date,
                    "domain": self.domain,
                }

                batch.set(doc_ref, data)

        batch.commit()
        print(f"Were pushed links to DB: {counter}")
