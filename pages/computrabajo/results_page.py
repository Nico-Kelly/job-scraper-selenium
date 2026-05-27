from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.models import JobPosting
from utils.logger import get_logger
import json

logger = get_logger(__name__)

class ComputrabajoResultsPage(BasePage):

    #locators

    JOB_CARD = (By.CSS_SELECTOR, '.job-card-placeholder')
    JOB_TITLE = (By.CSS_SELECTOR, '.title-placeholder')
    JOB_COMPANY = (By.CSS_SELECTOR, '.company-placeholder')
    JOB_LOCATION = (By.CSS_SELECTOR, '.location-placeholder')

    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        self.timeout = self.config['timeouts']['explicit_wait']

    
    def extract_job_cards(self):

        logger.info("Starting extraction of job cards from Computrabajo Results Page")

        extracted_jobs = []

        try:
            self.wait_visibility(self.JOB_CARD, timeout=self.timeout)
            cards = self.browser.find_elements(*self.JOB_CARD)

            logger.info(f"Found {len(cards)} job cards. Extracting data..")

            for card in cards:
                try:
                    title = card.find_element(*self.JOB_TITLE).text
                    company = card.find_element(*self.JOB_COMPANY).text
                    location = card.find_element(*self.JOB_LOCATION).text
                    url = card.find_element(*self.JOB_TITLE).get_attribute('href')

                    job = JobPosting(title=title, company=company, location=location, url=url)
                    extracted_jobs.append(job)

                except Exception as e:
                    logger.warning(f"Skipping a Computrabajo card due to missing data: {e}")
                    continue
        except TimeoutException:
            logger.error("No job cards found. The search might have yielded zero results or locators are wrong")
        return extracted_jobs