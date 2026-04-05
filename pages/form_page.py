from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from locators.form_page_locators import FormPageLocators

"""Методы для работы со страницей Form Fields"""
class FormPage(BasePage):

    """Ввод в поле Name"""
    def fill_name(self, text):
        self.input(FormPageLocators.NAME_INPUT, text)
        return self

    """Ввод пароля"""
    def fill_password(self, text):
        self.input(FormPageLocators.PASSWORD_INPUT, text)
        return self

    """Чекбокс Молоко"""
    def select_milk(self):
        self.click(FormPageLocators.DRINK_MILK_CHECKBOX)
        return self

    """Чекбокс Кофе"""
    def select_coffee(self):
        self.click(FormPageLocators.DRINK_COFFEE_CHECKBOX)
        return self

    """radio button Yellow"""
    def select_yellow(self):
        self.click(FormPageLocators.COLOR_YELLOW_RADIO)
        return self

    """Найти выпадающий список Automation"""
    def select_automation(self, value="undecided"):
        automation_select = Select(self.find(*FormPageLocators.AUTOMATION_SELECT))

        """Выбираем значение из списка"""
        automation_select.select_by_value(value)
        return self

    """Ввод емейла"""
    def fill_email(self, text):
        self.input(FormPageLocators.EMAIL_INPUT, text)
        return self

    """Получить элементы списка Automation tools"""
    def get_automation_tools(self):
        WebDriverWait(self.driver, 2).until(
            EC.presence_of_all_elements_located(
                FormPageLocators.AUTOMATION_TOOLS_ITEMS
            )
        )
        tools = self.finds(*FormPageLocators.AUTOMATION_TOOLS_ITEMS)

        """Вернет текст элементов из списка"""
        return [tool.text.strip() for tool in tools]

    """Получить список инструментов"""
    def build_message_from_tools(self):
        tools = self.get_automation_tools()

        """Найти инструмент с длинным названием"""
        longest_tool = max(tools, key=len)

        """Сформировать текст для Messege"""
        return f"{len(tools)}, {longest_tool}"

    """Ввод текста в Message"""
    def fill_message(self, text):
        self.input(FormPageLocators.MESSAGE_TEXTAREA, text)
        return self

    """Клик на кнопку Submit"""
    def submit(self):
        self.click(FormPageLocators.SUBMIT_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        return self

    """Ожидание alert и сразу получаем его объект"""
    def get_alert_text(self):
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        """Возвращаем текст alert"""
        return alert.text

    """Ожидание alert и сразу получаем его объект"""
    def accept_alert(self):
        # Ждем alert и сразу получаем его объект.
        alert = WebDriverWait(self.driver, 10).until(EC.alert_is_present())

        """Закрываем alert"""
        alert.accept()
        return self
