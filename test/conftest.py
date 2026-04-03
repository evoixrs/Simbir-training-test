
import logging

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.form_page import FormPage



"""Создал logger для проекта"""
logger = logging.getLogger("qa")

"""Параметры запуска pytest"""
def pytest_addoption(parser):

    """Адрес стенда"""
    parser.addoption("--base-url", action="store", default="https://practice-automation.com/form-fields/",
        help="Base URL of test stand")

    """Запуск без UI\GitHub Actions"""
    parser.addoption("--headless", action="store_true",
        help="Run browser in headless mode")


"""Фикстура вернёт базовый URL стенда из параметра pytest"""
@pytest.fixture
def base_url(request):
    url = request.config.getoption("--base-url")
    logger.info(f"Base URL: {url}")
    return url

"""Фикстура создает Chrome перед тестом и закроет после"""
@pytest.fixture
def driver(request):

    is_headless = request.config.getoption("--headless")
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if is_headless:
        chrome_options.add_argument("--headless=new")
    logger.info(f"Start browser. Headless = {is_headless}")
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    logger.info("Тест завершен. Закрываем браузер")
    driver.quit()

"""Фикстура создаст объект страницы FormPage"""
@pytest.fixture
def form_page(driver):
    logger.info("Создаем объект страницы FormPage")
    return FormPage(driver)
