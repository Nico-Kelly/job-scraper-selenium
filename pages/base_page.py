from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abc import ABC

class BasePage(ABC):
    
    def __init__(self, browser):
        self.browser = browser

    def wait_visibility(self, locator, timeout = 10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_multiple_visibility(self,locator,timeout = 10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))
    

    def type_text(self, locator, text):
        element = self.wait_visibility(locator)
        element.send_keys(text)


    def click_element(self, locator, timeout = 10):
        wait = WebDriverWait(self.browser, timeout)
        click_ec = wait.until(EC.element_to_be_clickable(locator))
        click_ec.click()