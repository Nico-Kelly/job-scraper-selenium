from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.models import JobPosting
from utils.logger import get_logger
import json
import time

logger = get_logger(__name__)

class LinkedInJobSearchPage(BasePage):
    
    #LOCATORs

    KEYWORD_INPUT = (By.CSS_SELECTOR, 'input[componentkey="jobSearchBox"]')
    LOCATION_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Ciudad, provincia o código postal"]') # This will only work as long as it is in spanish so i should change it soon
    
    #---

    JOB_LIST_PANEL = (By.CSS_SELECTOR, 'div[componentkey="SearchResultsMainContent"]')
    JOB_CARD = (By.CSS_SELECTOR, 'a[href*="/jobs/"]')
    JOB_TITLE = (By.CSS_SELECTOR, 'div[data-display-contents="true"] p span:first-child')
    JOB_COMPANY = (By.XPATH, './/div[p[contains(text(), "·")]]/p[1]')
    JOB_LOCATION = (By.XPATH, './/div[p[contains(text(), "·")]]/p[3]')


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
        

    def scroll_results_panel(self):

        try:

            panel = self.wait_visibility(self.JOB_LIST_PANEL, timeout=self.timeout)
            

            last_height= self.browser.execute_script("return arguments[0].scrollHeight", panel)

            while True:
                self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeigth", panel)

                time.sleep(1.5)

                new_height = self.browser.execute_script("return arguments[0].scrollHeight", panel)

                if new_height == last_height:
                    break
                last_height = new_height
            
            logger.info("Scroll completed.")

        except TimeoutException:
            logger.error("Scroll failed :c ")

    def extract_job_cards(self):
        extracted_jobs = []

        try:

            self.scroll_results_panel() # handle lazy loading

            
            self.wait_visibility(self.JOB_CARD, timeout=self.timeout)
            cards = self.browser.find_elements(*self.JOB_CARD)

            # iteration over cards to extract data
            for card in cards:
                try:
                    title = card.find_element(*self.JOB_TITLE).text
                    company = card.find_element(*self.JOB_COMPANY).text
                    location = card.find_element(*self.JOB_LOCATION).text

                    url = card.find_element(*self.JOB_TITLE).get_attribute('href')

                    job = JobPosting(title=title, company=company, location=location, url=url)
                    extracted_jobs.append(job)

                except Exception as e:
                    logger.warning(f"Skipping a card due to missing data: {e}")
                    continue
                    
        except TimeoutException:
            logger.error("No job cards found. The search might have yielded zero results or the page didn't load.")
    
        return extracted_jobs