from task_queue.tasks import nn_worker_task

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

    def __init__(self, id, link):
        super().__init__(link)
        self.id = id

        self.push_task_to_queue("text")

    def push_task_to_queue(self, text):
        """
        Push a task for asynchronous processing using Celery
        """
        result = nn_worker_task.apply_async(args=[self.id, text], queue='nn_worker')
        print(f'Task sent: {text}, Task ID: {result.id}')
