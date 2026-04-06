from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from locators.form_page_locators import FormPageLocators
from pages.base_page import BasePage


"""Методы заполняют поля формы с нужными опциями и строят цепочки вызовов"""
class FormPage(BasePage):

    def fill_name(self, text):
        self.input(FormPageLocators.NAME_INPUT, text)
        return self

    def fill_password(self, text):
        self.input(FormPageLocators.PASSWORD_INPUT, text)
        return self

    def select_milk(self):
        self.click(FormPageLocators.DRINK_MILK_CHECKBOX)
        return self

    def select_coffee(self):
        self.click(FormPageLocators.DRINK_COFFEE_CHECKBOX)
        return self

    def select_yellow(self):
        self.click(FormPageLocators.COLOR_YELLOW_RADIO)
        return self

    """Работа с выпадающим списком через Selenium Select"""
    def select_automation(self, value="undecided"):
        automation_select = Select(self.find(*FormPageLocators.AUTOMATION_SELECT))
        automation_select.select_by_value(value)
        return self

    def fill_email(self, text):
        self.input(FormPageLocators.EMAIL_INPUT, text)
        return self

    """Получение списка инструментов из Automation tools,
    ожидание появления элементов, забирает и очищает их текст"""

    def get_automation_tools(self):
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_all_elements_located(
                FormPageLocators.AUTOMATION_TOOLS_ITEMS
            )
        )
        tools = self.finds(*FormPageLocators.AUTOMATION_TOOLS_ITEMS)
        return [tool.text.strip() for tool in tools]

    """Собираем текст в Message:
    кол-во найденных инструментов и название самого длинного из них"""
    def build_message_from_tools(self):
        tools = self.get_automation_tools()
        longest_tool = max(tools, key=len)
        return f"{len(tools)}, {longest_tool}"

    def fill_message(self, text):
        self.input(FormPageLocators.MESSAGE_TEXTAREA, text)
        return self

    """Чтение текущего значения поля Message"""
    def get_message_value(self):
        return self.find(*FormPageLocators.MESSAGE_TEXTAREA).get_attribute("value")

    """Метод клика по кнопке, чтобы переиспользовать его в submit"""
    def click_submit(self):
        self.click(FormPageLocators.SUBMIT_BUTTON)
        return self

    """Отправка формы и ожидание alert как признака успешной отправки"""
    def submit(self):
        self.click_submit()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        return self

    """Методы для проверки валидации поля  Name в invalid test"""
    def get_name_required_error_text(self):
        return self.find(*FormPageLocators.NAME_REQUIRED_ERROR).text.strip()

    # validationMessage вернёт встроенное браузерное сообщение HTML5-валидации.
    def get_name_validation_message(self):
        return self.find(*FormPageLocators.NAME_INPUT).get_attribute(
            "validationMessage"
        )

    """Проверка какой элемент в фокусе после неуспешной отправки формы"""
    def get_active_element_id(self):
        return self.driver.switch_to.active_element.get_attribute("id")

    """Проверяем наличие alert без ожидания, если alert отсутствует, Selenium выбросит NoAlertPresentException"""
    def has_alert(self):
        try:
            self.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False

    """Работа с alert после успешной отправки формы, читает текст в нём"""
    def get_alert_text(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        return alert.text

    """Работа с alert, закрывает его"""
    def accept_alert(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert.accept()
        return self
