from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from pages.base_page import BasePage


class LinkedInFeedPage(BasePage):

    #URL

    URL = 'https://www.linkedin.com/feed/'

    #LOCATOR

    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-testid="typeahead-input"]')

    #INTERACTION METHODS

    def load(self):

        self.browser.get(self.URL)


    def search(self, phrase):
        self.type_text(self.SEARCH_INPUT, phrase + Keys.RETURN)

    def is_feed_loaded(self):
        #TODO
        pass
    
    def go_to_jobs_section(self):
        #TODO
        pass