from selenium.common.exceptions import NoSuchElementException

class BasePage():
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def is_element_present(self):
        try:
            self.browser.find_element(By.CSS_SELECTOR, "#login_link_invalid")
        except (NoSuchElementException):
            return False
        return True