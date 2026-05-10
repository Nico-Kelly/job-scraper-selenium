import os
import sys
import json

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.linkedin.login_page import LinkedInLogInPage
from pages.linkedin.search_page import LinkedInJobSearchPage
from services.csv_service import CSVService
from utils.logger import get_logger

with open('config/settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)

EXPLICIT_WAIT = settings['timeouts']['explicit_wait']

logger = get_logger(__name__)

def check_environment():
    """
    Validates the presence of required environment variables and configuration files.
    Exits the program immediately if any critical data (.env or settings.json) is missing,
    preventing unnecessary browser initialization.
    """
    logger.info("Validating environment and configurations...")
    load_dotenv()

    if not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'):
        logger.critical("Fatal error: missing credentials")
        sys.exit(1)

    if not os.path.exists('config/settings.json'):
        logger.critical("Fatal error: missing .json file")
        sys.exit(1)

    logger.info("All good.")

def setup_driver():
    """
    Configures and initializes the Selenium Chrome WebDriver.
    Sets up navigation rules such as maximizing the window and disabling notifications.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless")

    return webdriver.Chrome(options=options)

def main():
    """
    Main orchestrator function.
    Handles the execution flow: Environment validation, WebDriver setup,
    LinkedIn authentication, and executing the job search by-pass.
    Ensures safe teardown of resources in the finally block.
    """
    check_environment()
    logger.info("Starting Selenium")
    browser = setup_driver()

    logger.info("Initializing storage services...")
    export_folder = settings.get('export_folder', 'data_exports')
    csv_file = settings.get('csv_filename', 'ofertas_linkedin.csv')
    csv_service = CSVService(export_folder, csv_file)
    
    try:
        login_page = LinkedInLogInPage(browser)
        jobs_page = LinkedInJobSearchPage(browser)

        logger.info("Attempting login sequence")
        login_page.load()
        login_page.email(os.getenv('LINKEDIN_EMAIL'))
        login_page.password(os.getenv('LINKEDIN_PASSWORD'))
        login_page.click_sign_in()

        logger.info("Now loading jobs page")

        jobs_page.load()
        
    
        if jobs_page.is_search_page_loaded():
            logger.info("Success, searching for desired job")
            jobs_page.search()
            logger.info("Search sequence completed!")

            extracted_jobs = jobs_page.extract_job_cards()
            csv_service.append_jobs(extracted_jobs)

        else:
            logger.error("Job page failed to open")

    except Exception as e:
        logger.exception(f"Unexpected error occurred during execution: {e}")

    finally:
        logger.info("Turning down bot. Cleaning memory up.")
        browser.quit()

if __name__ == "__main__":
    main()