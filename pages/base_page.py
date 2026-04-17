from selenium.common.exceptions import ElementClickInterceptedException

from helpers.wait_helper import WaitHelper

"""Класс с общими действиями"""
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        """Создаем helper для явных ожиданий, чтобы использовать его во всех page object"""
        self.wait = WaitHelper(driver)

    """Возвращает один найденный элемент"""
    def find(self, by, value):
        return self.driver.find_element(by, value)

    """Возвращает список найденных элементов"""
    def finds(self, by, value):
        return self.driver.find_elements(by, value)

    """Клик с ожиданием кликабельности"""
    def click(self, locator, timeout=10):
        # Ждем, пока элемент станет видимым и доступным для клика.
        """Ожидаем кликабельность через WaitHelper вместо прямого WebDriverWait"""
        element = self.wait.element_clickable(locator, timeout)

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
        """Перед вводом ожидаем видимость поля, чтобы Selenium не вводил текст в еще неготовый элемент"""
        element = self.wait.element_visible(locator)
        element.clear()
        element.send_keys(text)

    """Открывает страницу по URL"""
    def open(self, url):
        self.driver.get(url)

    """Возвращает текущий URL страницы"""
    def get_current_url(self):
        return self.driver.current_url
