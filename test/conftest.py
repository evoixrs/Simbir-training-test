import logging
import shutil
import tempfile

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.form_page import FormPage


"""Общий логгер, пишем события старта браузера, завершения тестов и ошибки при сборе артефактов"""
logger = logging.getLogger("qa")

"""Задаются дополнительные параметры запуска тестов"""
def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="https://practice-automation.com/form-fields/",
        help="Base URL of test stand",)
    parser.addoption("--headless", action="store_true", default=False, help="Run Chrome in headless mode",)

"""Забираем base URL из параметров запуска pytest"""
@pytest.fixture
def base_url(request):
    url = request.config.getoption("--base-url")
    logger.info("Base URL: %s", url)
    return url

"""Создаем экземпляр ChromeDriver для каждого теста отдельно, 
не ждёт загрузку внешних ресурсов страницы, т.к без VPN не стабильно"""
@pytest.fixture
def driver(request):
    options = Options()
    options.page_load_strategy = "eager"

    """Отключаем браузерные уведомления, снижаем сетевую активность Chrome и работали стабильно"""
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-features=MediaRouter")
    profile_dir = None

    """Читаем флаг headless из CLI-опций pytest"""
    is_headless = request.config.getoption("--headless")
    logger.info("Start browser. Headless = %s", is_headless)

    """В headless создаем отдельный временный профиль Chrome"""
    if is_headless:
        profile_dir = tempfile.mkdtemp(prefix="chrome-headless-")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless=new")

        """Дополнительные флаги для стабильности запуска"""
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=0")
        options.add_argument(f"--user-data-dir={profile_dir}")

    """Настраиваем ChromeDriver и логи"""
    service = Service(
        service_args=["--verbose"],
        log_output="chromedriver.log",
    )

    """Запуск Chrome с подготовленными опциями и сервисом"""
    driver = webdriver.Chrome(service=service, options=options)
    # Ограничиваем слишком долгое ожидание загрузки страницы.
    driver.set_page_load_timeout(20)
    if not is_headless:
        driver.maximize_window()

    """Оключаем implicit wait"""
    driver.implicitly_wait(0)
    logger.info("Chrome started successfully")

    """Передаёт драйвер в тест, а после завершения возвращает"""
    yield driver

    """Закрываем браузер после каждого теста"""
    logger.info("Test finished. Closing browser")
    driver.quit()

    """Удаляем после теста временный профиль в headless"""
    if profile_dir:
        shutil.rmtree(profile_dir, ignore_errors=True)

"""Создает page object поверх уже готового драйвера с методами уровня страницы"""
@pytest.fixture
def form_page(driver):
    logger.info("Create FormPage instance")
    return FormPage(driver)

"""Отдает управление pytest, получаем отчёт о выполнении"""
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    """Если упала основная фаза выполнения теста, прикладывает артефакт"""
    if report.when != "call" or report.passed:
        return

    """Достаем драйвер из аргументов теста"""
    driver = item.funcargs.get("driver")
    if driver is None:
        return

    try:
        """Снимаем screenshot страницы и прикладываем в Allure"""
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        logger.warning("Failed to attach screenshot: %s", exc)

    try:
        """Дополнитель прикладываем HTML страницы на момент падения"""
        allure.attach(
            driver.page_source,
            name="page-source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:
        logger.warning("Failed to attach page source: %s", exc)
