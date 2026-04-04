from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовые методы для работы со страницами."""

    def __init__(self, driver):
        # Сохраняем экземпляр браузера, с которым будет работать page object.
        self.driver = driver

    def find(self, by, value):
        # Возвращаем один найденный элемент.
        return self.driver.find_element(by, value)

    def finds(self, by, value):
        # Возвращаем список найденных элементов.
        return self.driver.find_elements(by, value)

    def click(self, locator, timeout=10):
        # Ждем, пока элемент станет кликабельным.
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

        # Прокручиваем страницу так, чтобы элемент оказался в видимой области.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

        try:
            # Сначала используем обычный Selenium click,
            # потому что он ближе к реальному пользовательскому действию.
            element.click()
        except ElementClickInterceptedException:
            # Если клик перехвачен другим элементом или слоем,
            # пробуем еще раз аккуратно подвести элемент в область видимости.
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", element
            )

            # JS click используем как запасной вариант,
            # когда обычный click не проходит из-за особенностей верстки.
            self.driver.execute_script("arguments[0].click();", element)

    def input(self, locator, text):
        # Находим поле ввода.
        element = self.find(*locator)

        # Очищаем текущее значение поля.
        element.clear()

        # Вводим новый текст.
        element.send_keys(text)

    def open(self, url):
        # Открываем нужную страницу.
        self.driver.get(url)

    def get_current_url(self):
        # Возвращаем текущий адрес страницы.
        return self.driver.current_url