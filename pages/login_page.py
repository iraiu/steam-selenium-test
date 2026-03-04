from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    PAGE_UNIQUE_ELEMENT = (By.XPATH, "//input[@type='password']")
    USERNAME_FIELD = (By.XPATH, "//div[contains(text(), 'имя аккаунта')]/following-sibling::input")
    PASSWORD_FIELD = (By.XPATH, "//div[contains(text(), 'Пароль')]/following-sibling::input")
    SIGN_IN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    LOADING_INDICATOR = (By.XPATH, "//button[text()='Войти']/div/div")
    ERROR_MESSAGE = (By.XPATH, "//form[.//button[@type='submit']]//div[.//button[@type='submit']]/following-sibling::div[1]")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_credentials(self, username, password):
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_FIELD)).send_keys(
            username)
        self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)).send_keys(
            password)

    def click_sign_in(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SIGN_IN_BUTTON)).click()

    def is_loading_indicator_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.LOADING_INDICATOR))
            return True
        except Exception:
            return False

    def wait_for_loading_to_disappear(self):
        self.wait.until_not(
            EC.visibility_of_element_located(self.LOADING_INDICATOR))

    def get_error_message_text(self):
        return self.wait.until(
            EC.presence_of_element_located(self.ERROR_MESSAGE)).text
