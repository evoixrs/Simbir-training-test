from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

"""Класс с общими действиями"""
class BasePage:
    def __init__(self, driver):
        self.driver = driver

    """Возвращает один найденный элемент"""
    def find(self, by, value):
        return self.driver.find_element(by, value)

    """Возвращает список найденных элементов"""
    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    """Клик с ожиданием кликабельности"""
    def click(self, locator, timeout=10):
        # Ждем, пока элемент станет видимым и доступным для клика.
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

        """Скролл страницы, чтобы элемент оказался в зоне видимости"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        try:
            """Сначала используем обычный Selenium click"""
            element.click()
        except ElementClickInterceptedException:

            """Если клик перехватил другой элемент, пробуем клик через JavaScript"""
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", element
            )
            self.driver.execute_script("arguments[0].click();", element)

    """Вводит текст в поле после очистки текущего значения"""
    def input(self, locator, text):
        element = self.find(*locator)
        element.clear()
        element.send_keys(text)

    """Открывает страницу по URL"""
    def open(self, url):
        self.driver.get(url)

    """Возвращает текущий URL страницы"""
    def get_current_url(self):
        return self.driver.current_url
