from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.models import JobPosting
import json

class LinkedInJobSearchPage(BasePage):
    
    #LOCATORs

    KEYWORD_INPUT = (By.CSS_SELECTOR, 'input[componentkey="jobSearchBox"]')
    LOCATION_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Ciudad, provincia o código postal"]') # This will only work as long as it is in spanish so i should change it soon
    
    #---

    JOB_CARD = (By.CSS_SELECTOR, 'TODO')
    JOB_TITLE = (By.CSS_SELECTOR, 'TODO')
    JOB_COMPANY = (By.CSS_SELECTOR, 'TODO')
    JOB_LOCATION = (By.CSS_SELECTOR, 'TODO')


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
        

    def extract_job_cards(self):
        extracted_jobs = []

        try:

            self.wait_visibility(self.JOB_CARD, timeout=self.timeout)

            cards = self.browser.find_elements(*self.JOB_CARD)


            # iteraterion over cards to extract data

            for card in cards:
                try:

                    title = card.find_element(*self.JOB_TITLE).text
                    company = card.find_element(*self.JOB_COMPANY).text
                    location = card.find_element(*self.JOB_LOCATION).text

                    url = card.find_element(*self.JOB_TITLE).get_attribute('href')

                    job = JobPosting(title=title, company=company, location=location, url=url)
                    extracted_jobs.append(job)


                except Exception as e:
                    print(f"Skipping a card due to missing data: {e}")
                    continue
        except TimeoutException:
            print("No job cards found. The search migh have yielded zero results or the page didn't load.")
    
        return extracted_jobs
    
