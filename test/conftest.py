import logging
# Подключаем стандартный модуль logging, чтобы писать технические сообщения в лог.

import pytest
# Pytest нужен для фикстур и пользовательских CLI-опций.

from selenium import webdriver
# Основной модуль Selenium WebDriver для создания экземпляра браузера.

from selenium.webdriver.chrome.options import Options
# Класс Options нужен для передачи аргументов запуска Chrome.

from selenium.webdriver.chrome.service import Service
# Service управляет запуском локального ChromeDriver и его логированием.

from pages.form_page import FormPage
# Импортируем Page Object страницы формы, чтобы использовать его в фикстуре form_page.


logger = logging.getLogger("qa")
# Создаем именованный логгер "qa".
# Через него будем писать служебные сообщения о запуске браузера и работе фикстур.


def pytest_addoption(parser):
    # Эта функция добавляет кастомные параметры командной строки для pytest.

    parser.addoption(
        "--base-url",
        action="store",
        default="https://practice-automation.com/form-fields/",
        help="Base URL of test stand",
    )
    # Добавляем параметр --base-url.
    # Он позволяет передавать адрес тестового стенда при запуске тестов.
    # Если параметр не передан, используется значение по умолчанию.

    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode",
    )
    # Добавляем флаг --headless.
    # Если он указан, браузер будет запускаться без окна.
    # Если флаг не указан, остается режим по умолчанию — headed.


@pytest.fixture
def base_url(request):
    # Фикстура base_url получает значение CLI-параметра --base-url.

    url = request.config.getoption("--base-url")
    # Читаем переданный base URL из конфигурации pytest.

    logger.info("Base URL: %s", url)
    # Пишем в лог, какой base URL реально используется в запуске.

    return url
    # Возвращаем URL в тесты или другие фикстуры.


@pytest.fixture
def driver(request):
    # Главная фикстура для создания и закрытия браузера.

    options = Options()
    # Создаем объект Chrome Options, куда будем складывать аргументы запуска Chrome.

    options.add_argument("--disable-notifications")
    # Отключаем браузерные уведомления, чтобы они не мешали тестам.

    is_headless = request.config.getoption("--headless")
    # Получаем значение флага --headless из параметров запуска pytest.

    logger.info("Start browser. Headless = %s", is_headless)
    # Логируем, в каком режиме будет стартовать браузер: headed или headless.

    if is_headless:
        # Если флаг --headless передан, запускаем браузер в headless-режиме.

        options.add_argument("--window-size=1920,1080")
        # Для headless явно задаем размер окна,
        # чтобы layout страницы был предсказуемым.

        options.add_argument("--headless=new")
        # Включаем новый headless-режим Chrome.

        options.add_argument("--no-sandbox")
        # Отключаем sandbox.
        # Часто помогает в Linux/CI-окружениях, где без этого Chrome может не стартовать.

        options.add_argument("--disable-dev-shm-usage")
        # Убираем зависимость от /dev/shm.
        # Это часто используют, когда браузеру не хватает shared memory.

        options.add_argument("--remote-debugging-pipe")
        # Включаем режим удаленной отладки через pipe.
        # Это один из практических способов уменьшить проблемы запуска вокруг DevToolsActivePort.

    service = Service(
        service_args=["--verbose"],
        log_output="chromedriver.log",
    )
    # Создаем Service для ChromeDriver.
    # --verbose включает подробный лог драйвера.
    # log_output="chromedriver.log" пишет этот лог в файл chromedriver.log.

    driver = webdriver.Chrome(service=service, options=options)
    # Запускаем ChromeDriver и создаем экземпляр браузера Chrome
    # с указанными options и service.

    if not is_headless:
        driver.maximize_window()
        # В обычном режиме разворачиваем окно браузера на весь экран.

    driver.implicitly_wait(0)
    # Явно отключаем implicit wait.
    # Это полезно, если в проекте ставка делается на explicit wait.

    logger.info("Chrome started successfully")
    # Если дошли до этой строки — браузер успешно стартовал.

    yield driver
    # Отдаем браузер тесту.
    # После завершения теста выполнение продолжится ниже, в teardown-части фикстуры.

    logger.info("Test finished. Closing browser")
    # Логируем завершение теста и начало закрытия браузера.

    driver.quit()
    # Полностью закрываем браузер и завершаем сессию WebDriver.


@pytest.fixture
def form_page(driver):
    # Фикстура создает объект страницы формы на основе уже запущенного браузера.

    logger.info("Create FormPage instance")
    # Пишем в лог, что создается экземпляр FormPage.

    return FormPage(driver)
    # Возвращаем page object, чтобы тесты работали не с "сырым" драйвером,
    # а с объектом страницы.
