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
    #TODO
    pass

if __name__ == "__main__":
    main()