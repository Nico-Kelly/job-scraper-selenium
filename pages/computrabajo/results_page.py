from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.models import JobPosting
from utils.logger import get_logger
import json
import time

logger = get_logger(__name__)

class ComputrabajoResultsPage(BasePage):

    #locators

    JOB_CARD = (By.CSS_SELECTOR, '.box_offer.sel')
    JOB_TITLE = (By.CSS_SELECTOR, '.js-o-link.fc_base')
    JOB_COMPANY = (By.CSS_SELECTOR, '.fc_base.t_ellipsis')
    JOB_LOCATION = (By.CSS_SELECTOR, '.mr10')

    #pagination locators
    NEXT_BUTTON = (By.CSS_SELECTOR, '.b_primary.w48.buildLink.cp')

    def __init__(self, browser):
        super().__init__(browser)
        with open('config/settings.json', 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        self.timeout = self.config['timeouts']['explicit_wait']
        self.max_pages = self.config.get('max_pages', 1)


    def extract_job_cards(self):

        logger.info("Starting extraction of job cards from Computrabajo Results Page")
        extracted_jobs = []
        current_page = 1

        while current_page <= self.max_pages:
            logger.info(f"---Scraping page {current_page} of {self.max_pages}")

            try:
                self.wait_visibility(self.JOB_CARD, timeout=self.timeout)
                cards = self.browser.find_elements(*self.JOB_CARD)
                logger.info(f"Found {len(cards)} job cards on page {current_page} Extracting data..")

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
                break



            if current_page < self.max_pages:

                try:
                    logger.info("Looking for the 'next' button to turn page...")
                    next_btn = self.wait_visibility(self.NEXT_BUTTON, timeout= self.timeout)
                    next_btn.click()
                    time.sleep(2)
                except TimeoutException:
                    logger.info("No 'Next' button found. Reached the las page of the results")
                    break
            current_page += 1

        logger.info(f"Extraction completed. total jobs scraped: {len(extracted_jobs)}")
        return extracted_jobs



