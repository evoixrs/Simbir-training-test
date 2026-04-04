from selenium.webdriver.common.by import By

"""Нужные локаторы для теста"""
class FormPageLocators:
    NAME_INPUT = (By.ID, "name-input")

    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")

    DRINK_MILK_CHECKBOX = (By.ID, "drink2")

    DRINK_COFFEE_CHECKBOX = (By.ID, "drink3")

    COLOR_YELLOW_RADIO = (By.ID, "color3")

    AUTOMATION_SELECT = (By.ID, "automation")
    AUTOMATION_TOOLS_ITEMS = (By.CSS_SELECTOR, "label + ul li")

    EMAIL_INPUT = (By.ID, "email")

    MESSAGE_TEXTAREA = (By.ID, "message")

    SUBMIT_BUTTON = (By.ID, "submit-btn")


