from .base_page import BasePage
from selenium.webdriver.common.by import By
from .locators import MainPageLocators
from .login_page import LoginPage


class MainPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)

    def open_cart(self):
        link = self.browser.find_element(*MainPageLocators.CLICK_CART)
        link.click()

    def should_be_empty_basket(self):
        assert self.is_not_element_present(*MainPageLocators.BASKET_ITEMS), \
                "Basket items are present, but should not be"
        assert self.is_element_present(*MainPageLocators.EMPTY_BASKET_MESSAGE), \
                "Empty basket message is not present"

