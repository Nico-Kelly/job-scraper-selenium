import os
import sys
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.linkedin.login_page import LinkedInLogInPage
from pages.linkedin.search_page import LinkedInJobSearchPage

def check_enviroment():
    print("validating env file")

    load_dotenv()

    if not os.getenv('LINKEDIN_EMAIL') or not os.getenv('LINKEDIN_PASSWORD'):
        print("Fatal error missing credentials")
        sys.exit(1)

    if not os.path.exists('config/settings.json'):
        print("Fatal error missing .env file")
        sys.exit(1)

    print("All good.")

def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--headless")

    return webdriver.Chrome(options=options)

def main():
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

        time.sleep(3)

        print("Now loading jobs page")
        jobs_page.load()
        if jobs_page.is_search_page_loaded():
            print("Success, searching for desired job")
            jobs_page.search()
            print("Completed! wait 5 seconds.")
            time.sleep(5)
        else:
            print("Job page failed to open")

    except Exception as e:
        print(f"Unexpected error ocurred during: {e}")

    finally:
        print("Turning down bot. cleaning memory up.")
        browser.quit()




if __name__ == "__main__":
    main()