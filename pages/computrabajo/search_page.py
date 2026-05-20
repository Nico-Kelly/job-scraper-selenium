from pages.base_page import BasePage
from utils.logger import get_logger
import json

logger = get_logger(__name__)

class ComputrabajoSearchPage(BasePage):
    
    # LOCATORS
    # TODO
    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)

        self.url = self.config['urls']['computabrajo']
        self.keyword = self.config['search_params']['job_title']
        self.location = self.config['search_params']['location']
        self.timeout = self.config['timeouts']['explicit_wait']

    def load(self):
        logger.info(f"Loading Computrabajo {self.url}")
        self.browser.get(self.url)


    def search(self):
        # TODO: 
        pass
        
    def extract_job_cards(self):
        # TODO: 
        return []