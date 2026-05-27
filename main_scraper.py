import os
import sys
import json

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.linkedin.login_page import LinkedInLogInPage
from pages.linkedin.search_page import LinkedInJobSearchPage
from pages.computrabajo.search_page import ComputrabajoSearchPage
from pages.computrabajo.results_page import ComputrabajoResultsPage
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

def setup_driver(driver_config):
    """
    Configures and initializes the Selenium Chrome WebDriver.
    Sets up navigation rules such as maximizing the window and disabling notifications.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless")

    # --- ANTI-BOT MEASURES ---
    # Removes the "Chrome is being controlled by automated software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Disables internal blink features that reveal Selenium
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Use a standard user-agent to look like a normal user
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    if driver_config.get('headless_mode', False):
        logger.info("Headless mode is ENABLED")
        options.add_argument("--headless=new")  # Modern headless mode for Chrome

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

    driver_config = settings.get('driver_config', {})
    browser = setup_driver(driver_config)

    logger.info("Initializing storage services...")
    export_folder = settings.get('export_folder', 'data_exports')
    csv_file = settings.get('csv_filename', 'scraped_jobs.csv')
    csv_service = CSVService(export_folder, csv_file)

    target_portal = settings.get('target_portal', 'linkedin')
    
    try:
        if target_portal == 'linkedin':
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

        elif target_portal == 'computrabajo':
            
            search_page = ComputrabajoSearchPage(browser)
            results_page = ComputrabajoResultsPage(browser)

            logger.info("Loading Computrabajo jobs page")
            search_page.load()
            search_page.search()

            logger.info("Search executed, passing control to Results page")
            extracted_jobs = results_page.extract_job_cards()
            csv_service.append_jobs(extracted_jobs)


        else:
            logger.error(f"Portal '{target_portal} is not supported yet :)'")
    except Exception as e:
        logger.exception(f"Unexpected error occurred during execution: {e}")

    finally:
        logger.info("Turning down bot. Cleaning memory up.")
        browser.quit()

if __name__ == "__main__":
    main()