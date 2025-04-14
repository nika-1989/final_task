from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators

#Все методы для работы с элементами принимают параметры how (тип локатора) и what (значение локатора)
#Предоставляет три основных варианта проверки элементов: Наличие на странице, Отсутствие на странице, Исчезновение со страницы
#Этот класс является базовым и должен наследоваться другими page-объектами для конкретных страниц.

class BasePage():
    def __init__(self, browser, url, timeout=10): #инициализирует страницу с браузером и URL
        self.browser = browser #экземпляр веб-драйвера
        self.url = url #URL страницы
        self.browser.implicitly_wait(timeout) #неявное ожидание элементов

    def open(self):
        self.browser.get(self.url) #открывает указанный урл в браузере

# провеяет налииче элемента на странице, если элемент найден, возвращает true
    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

#проверяет отсутсвие элемента на странице течение заданного времени
#использует явное ожидание (explicit wait)
#возвращает true, если элемент НЕ появился за указанное время (4сек)
    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

#проверяет, что элемент исчезает со страницы в течение заданного времени
#возвращает true, если элемент исчез, false, если остался
    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    def go_to_login_page(self):
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()
        from .login_page import LoginPage  # Импорт здесь, чтобы избежать циклического импорта
        return LoginPage(self.browser, self.browser.current_url)  # Возвращаем объект LoginPage

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def go_to_basket_page(self):
        basket_link = self.browser.find_element(*BasePageLocators.BASKET_LINK)
        basket_link.click()
        from .basket_page import BasketPage
        return BasketPage(self.browser, self.browser.current_url)

    def should_be_authorized_user(self):
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                     " probably unauthorised user"



