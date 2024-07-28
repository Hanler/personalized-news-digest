from task_queue.tasks import process_task

import os
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
from config.settings import CHROMEDRIVER_PATH, CHROME_PATH

class ArticleScraper(object):

    """
    A class used to represent an article scraper that processes
    the page and extracts the article,
    then sends a task for asynchronous processing
    """

    def __init__(self, link):       
        self.link = link

        # Define driver's options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Define driver
        self.driver = uc.Chrome(options=options, driver_executable_path=CHROMEDRIVER_PATH, browser_executable_path=CHROME_PATH)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.get_source_html()

    def get_source_html(self):
        try:
            self.driver.get(self.link)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            page_source = self.driver.page_source
            print(f"page_source: {page_source}")

            soup = BeautifulSoup(page_source, "html.parser")

            for tag in soup(
                ["header", "style", "footer", "head", "script", "iframe", "noscript", "svg"]
            ):
                tag.decompose()

            links = [a["href"] for a in soup.find_all("a", href=True)]

            print(links)

            # temp_links = set(links)
            # links = list(temp_links)
            # changed_links = []

            # domain = urlparse(url).netloc

            # for link in links:
            #     if link.startswith("#"):
            #         continue
            #     if link.startswith("?"):
            #         continue
            #     if link.startswith("/"):
            #         changed_link = urljoin(url, link)
            #         if urlparse(changed_link).netloc == domain:
            #             changed_links.append(changed_link)
            #     elif urlparse(link).netloc == domain:
            #         changed_links.append(link)

            # # DELETE LATER
            # # ------------
            # with open("0.2_links.txt", "w", encoding="utf-8") as file:
            #     for link in changed_links:
            #         file.write(link + "\n")
            # # ------------


        except Exception as _ex:
            print(_ex)

        # return changed_links
        return links

    def send_task(self, task):
        """
        Sends a task for asynchronous processing using Celery
        """
        result = process_task.delay(task)
        print(f'Task sent: {task}, Task ID: {result.id}')
