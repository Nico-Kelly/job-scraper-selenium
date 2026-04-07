from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from pages.base_page import BasePage


class LinkedInFeedPage(BasePage):

    #URL

    URL = 'https://www.linkedin.com/feed/'

    #LOCATORs

    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-testid="typeahead-input"]')
    JOBS_NAV_ICON = (By.CSS_SELECTOR, "a[href*='/jobs/']")
    #INTERACTION METHODS

    def load(self):
        self.browser.get(self.URL)


    def search(self, phrase):
        self.type_text(self.SEARCH_INPUT, phrase + Keys.RETURN)

    def is_feed_loaded(self):
        #TODO
        pass
    
    def go_to_jobs_section(self):
        self.click_element(self.JOBS_NAV_ICON)