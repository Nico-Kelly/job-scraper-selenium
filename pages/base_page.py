from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, browser):
        self.browser = browser

    def wait_visibility(self, locator, timeout = 10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_multiple_visibility(self,locator,timeout = 10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))
    

