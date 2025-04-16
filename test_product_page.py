import pytest
import time
from .pages.locators import ProductPageLocators
from .pages.product_page import ProductPage
from .pages.login_page import LoginPage

#["http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer0",
                              #"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
                              #"http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer2",
                             # "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer3",
                            #  "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer4",
                             # "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer5",
                             # "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer6",
                             # pytest.param("http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
                         # marks=pytest.mark.xfail),
                             # "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer8",
                             # "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer9"])
#link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"
link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
@pytest.mark.need_review
def test_guest_can_add_product_to_basket(browser):
    link = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"
    page = ProductPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    # Получаем название и цену товара
    expected_name = page.get_product_name()
    expected_price = page.get_product_price()
    page.add_to_cart()  # выполняем метод страницы — добавление в корзину
    page.solve_quiz_and_get_code()
    page.should_be_product_added(expected_name, expected_price)

@pytest.mark.need_review
@pytest.mark.xfail
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser):
    page = ProductPage(browser, link)  # инициализируем Page Object, передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.add_to_cart() #добавляем товар в корзину
    page.should_not_be_success_message()

@pytest.mark.xfail
def test_guest_cant_see_success_message(browser):
    page = ProductPage(browser, link)
    page.open()
    page.should_not_be_success_message()

@pytest.mark.xfail(reason="Сообщение не должно исчезать сразу")
def test_message_disappeared_after_adding_product_to_basket(browser):
        page = ProductPage(browser, link)
        page.open()
        page.add_to_cart()
        assert page.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Сообщение об успехе не исчезло, но должно было"

def test_guest_should_see_login_link_on_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    page.should_be_login_link()

@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
    page = ProductPage(browser, link)
    page.open()
    login_page = page.go_to_login_page()  # Теперь получаем объект LoginPage
    login_page.should_be_login_page()  # Проверяем все аспекты страницы логина

class TestUserAddToBasketFromProductPage:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        login_page = LoginPage (browser, "http://selenium1py.pythonanywhere.com/accounts/login/")
        login_page.open()
        # Регистрируем нового пользователя
        email = f"user{str(time.time())}@example.com"
        password = "SecurePass123"
        login_page.register_new_user(email, password)
        # Проверяем, что пользователь залогинен
        login_page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser):
        page = ProductPage(browser, link)
        page.open()
        page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        page = ProductPage(browser, link)
        page.open()
        expected_name = page.get_product_name()
        expected_price = page.get_product_price()
        page.add_to_cart()
        page.should_be_product_added(expected_name, expected_price)
