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

from scrapers.Scraper import Scraper

class ArticleScraper(Scraper):

    """
    A class used to represent an article scraper that processes
    the page and extracts the article,
    then sends a task for asynchronous processing
    """

    def __init__(self, link):       
        super().__init__(link)

    def get_source_html(self):
        try:

            links = [a["href"] for a in self.soup.find_all("a", href=True)]

            temp_links = set(links)
            links = list(temp_links)
            changed_links = []

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
