import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: '--browser_name=chrome' or '--browser_name=firefox'")
    parser.addoption('--language', action='store', default='en',
                     help="Choose language: '--language=en' or '--language=ru'")

@pytest.fixture(scope="function")
def browser(request):
    # Получаем параметры из командной строки
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    # Инициализация браузера
    browser = None
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = webdriver.ChromeOptions()
        options.add_argument(f"--lang={user_language}")  # Устанавливаем язык браузера
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)  # Устанавливаем язык браузера
        browser = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError("--browser_name should be 'chrome' or 'firefox'")

    yield browser

    # Завершение работы браузера
    print("\nquit browser..")
    browser.quit()