from selenium.webdriver.common.by import By

"""Нужные локаторы для теста"""
class FormPageLocators:
    NAME_INPUT = (By.ID, "name-input")
    NAME_REQUIRED_ERROR = (By.XPATH, "//input[@id='name-input']/following::p[contains(@class, 'red_txt')][1]")

    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")

    """Формирует локатор checkbox по тексту напитка, чтобы не привязываться к id drink2/drink3"""
    @staticmethod
    def drink_checkbox(drink_name):
        return (
            By.XPATH,
            f"//label[normalize-space()='{drink_name}']/preceding-sibling::input[@type='checkbox'][1]",
        )

    """Формирует локатор radio button по тексту цвета, чтобы не привязываться к id color3"""
    @staticmethod
    def color_radio(color_name):
        return (
            By.XPATH,
            f"//label[normalize-space()='{color_name}']/preceding-sibling::input[@type='radio'][1]",
        )

    AUTOMATION_SELECT = (By.ID, "automation")
    AUTOMATION_TOOLS_ITEMS = (By.CSS_SELECTOR, "label + ul li")

    EMAIL_INPUT = (By.ID, "email")

    MESSAGE_TEXTAREA = (By.ID, "message")

    SUBMIT_BUTTON = (By.ID, "submit-btn")


