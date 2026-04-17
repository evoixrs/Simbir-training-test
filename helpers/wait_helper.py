from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


"""Класс собирает явные ожидания в одном месте, чтобы не дублировать WebDriverWait в page object"""
class WaitHelper:
    def __init__(self, driver, timeout=10):
        """Сохраняем driver и общий timeout по умолчанию для всех ожиданий"""
        self.driver = driver
        self.timeout = timeout

    """Ожидает появления одного элемента в DOM"""
    def element_present(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    """Ожидает появления списка элементов в DOM"""
    def elements_present(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    """Ожидает, что элемент появился на странице и стал видимым"""
    def element_visible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    """Ожидает, что элемент доступен для клика"""
    def element_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    """Ожидает появления alert после отправки формы"""
    def alert_present(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.alert_is_present()
        )
