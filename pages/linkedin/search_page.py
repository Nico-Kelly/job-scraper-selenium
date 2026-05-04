from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import json

class LinkedInJobSearchPage(BasePage):
    
    #LOCATORs

    KEYWORD_INPUT = (By.CSS_SELECTOR, 'input[componentkey="jobSearchBox"]')
    LOCATION_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Ciudad, provincia o código postal"]') # This will only work as long as it is in spanish so i should change it soon
    
    #INTERACTION METHODS

    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)

        self.url = self.config['urls']['linkedin']
        self.keyword = self.config['search_params']['job_title']
        self.location = self.config['search_params']['location']
        self.timeout = self.config['timeouts']['explicit_wait']

    def load(self):
        self.browser.get(self.url)

    def search(self):
        self.type_text(self.KEYWORD_INPUT, self.keyword)
        self.type_text(self.LOCATION_INPUT, self.location + Keys.RETURN)

    def is_search_page_loaded(self):
        try:

            self.wait_visibility(self.KEYWORD_INPUT, timeout=self.timeout)
            return True
        except TimeoutException:
            return False
        
