import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from config.settings import CHROMEDRIVER_PATH, CHROME_PATH, USELESS_TAGS


class Scraper(object):
    def __init__(self, link):
        self.link = link

        # Define driver's options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Define driver
        self.driver = uc.Chrome(options=options, driver_executable_path=CHROMEDRIVER_PATH, browser_executable_path=CHROME_PATH)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Call function
        self.soup = self.get_source_html()

    def get_source_html(self):
        try:
            self.driver.get(self.link)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            page_source = self.driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")

            soup = self.remove_useless_tags(USELESS_TAGS, soup)
        
        except Exception as _ex:
            # print(_ex)
            soup = None

        return soup
    
    def remove_useless_tags(self, tags, soup):
        for tag in soup(tags):
            tag.decompose()

        return soup
