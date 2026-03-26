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
        search_input = self.wait_visibility(self.SEARCH_INPUT)
        search_input.send_keys(phrase + Keys.RETURN)