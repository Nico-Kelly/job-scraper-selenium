from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from pages.base_page import BasePage
import json

class LinkedInJobSearchPage(BasePage):

    #URL

    URL = 'https://www.linkedin.com/jobs/'

    #LOCATORs

    KEYWORD_INPUT = ()
    LOCATION_INPUT = ()
    
    #INTERACTION METHODS

    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r') as file:
            self.config = json.load(file)

        self.url = self.config['urls']['linkedin']
        self.keyword = self.config['search_params']['job_title']
        self.location = self.config['search_params']['location']

    def load(self):
        self.browser.get(self.URL)

    def search(self, phrase):
        self.type_text(self.SEARCH_INPUT, phrase + Keys.RETURN)

    def is_search_page_loaded(self):
        #TODO
        pass