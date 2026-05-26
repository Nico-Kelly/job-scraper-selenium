from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.logger import get_logger
import json

logger = get_logger(__name__)

class ComputrabajoSearchPage(BasePage):
    
    # LOCATORS
    KEYWORD_INPUT = (By.CSS_SELECTOR, '#search-job-input-placeholder') 
    LOCATION_INPUT = (By.CSS_SELECTOR, '#search-location-input-placeholder')
    JOB_CARD = (By.CSS_SELECTOR, '.job-card-placeholder')

    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)

        self.url = self.config['urls']['computrabajo']
        self.keyword = self.config['search_params']['job_title']
        self.location = self.config['search_params']['location']
        self.timeout = self.config['timeouts']['explicit_wait']

    def load(self):
        logger.info(f"Loading Computrabajo {self.url}")
        self.browser.get(self.url)


    def search(self):
        logger.info("Initiatin search sequence on Computrabajo")
        try:
            self.wait_visibility(self.KEYWORD_INPUT, timeout=self.timeout)
            self.type_text(self.KEYWORD_INPUT, self.keyword)
            self.type_text(self.LOCATION_INPUT, self.location + Keys.RETURN)

        except TimeoutException:
            logger.error("Could not find search elements. DOM locators need to be updated")
            raise
        
    def extract_job_cards(self):
        # TODO: 
        return []