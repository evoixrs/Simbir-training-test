from selenium.webdriver.common.by import By


class FormPageLocators:
    NAME_INPUT = (By.ID, "name-input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    RESULT_TEXT = (By.ID, "feedback")
