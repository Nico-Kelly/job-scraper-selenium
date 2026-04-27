from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class LinkedInLogInPage(BasePage):

    #URL

    URL = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

    #LOCATOR

    EMAIL_INPUT = (By.ID, "username")

    PASSWORD_INPUT = (By.ID, "password")

    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    #INTERACTION METHODS

    def load(self):

        self.browser.get(self.URL)


    def email(self, mail):
        self.type_text(self.EMAIL_INPUT,mail)

    def password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)


    def click_sign_in(self):
        self.click_element(self.SIGN_IN_BUTTON.click())
        
        