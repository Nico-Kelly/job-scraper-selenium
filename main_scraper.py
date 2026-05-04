import os
import sys
import time
import json

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.linkedin.login_page import LinkedInLogInPage
from pages.linkedin.search_page import LinkedInJobSearchPage


with open('config/settings.json', 'r', encoding='utf-8') as f:
    settings = json.load(f)


    EXPLICIT_WAIT = settings['timeouts']['explicit_wait']
def check_enviroment():
    """
        Validates the presence of required environment variables and configuration files.
        Exits the program immediately if any critical data (.env or settings.json) is missing,
        preventing unnecessary browser initialization.
        """

    print("Validating environment and configurations...")

    load_dotenv()

    if not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'):
        print("Fatal error missing credentials")
        sys.exit(1)

    if not os.path.exists('config/settings.json'):
        print("Fatal error missing .json file")
        sys.exit(1)

    print("All good.")

def setup_driver():
    """
        Configures and initializes the Selenium Chrome WebDriver.
        Sets up navigation rules such as maximizing the window and disabling notifications.
    """

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    #options.add_argument("--headless")

    return webdriver.Chrome(options=options)

def main():
    """
        Main orchestrator function.
        Handles the execution flow: Environment validation, WebDriver setup,
        LinkedIn authentication, and executing the job search by-pass.
        Ensures safe teardown of resources in the finally block.
    """


    check_enviroment()
    print("Starting Selenium")
    browser = setup_driver()

    try:
        login_page = LinkedInLogInPage(browser)
        jobs_page = LinkedInJobSearchPage(browser)

        print("Login in")
        login_page.load()
        login_page.email(os.getenv('LINKEDIN_EMAIL'))
        login_page.password(os.getenv('LINKEDIN_PASSWORD'))
        login_page.click_sign_in()

        time.sleep(EXPLICIT_WAIT)

        print("Now loading jobs page")
        jobs_page.load()
        if jobs_page.is_search_page_loaded():
            print("Success, searching for desired job")
            jobs_page.search()
            print("Completed! wait 5 seconds.")
            time.sleep(EXPLICIT_WAIT)
        else:
            print("Job page failed to open")

    except Exception as e:
        print(f"Unexpected error ocurred during: {e}")

    finally:
        print("Turning down bot. cleaning memory up.")
        browser.quit()




if __name__ == "__main__":
    main()