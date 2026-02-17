from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:

    HOME_PAGE_CONTENT = (By.CSS_SELECTOR, "img[alt='STEAM']")
    LOGIN_BUTTON = (By.XPATH, "//a[contains(text(), 'вход')]")
    USERNAME_FIELD = (
        By.XPATH,
        "//div[contains(text(), 'имя аккаунта')]/following-sibling::input",
    )
    PASSWORD_FIELD = (
        By.XPATH,
        "//div[contains(text(), 'Пароль')]/following-sibling::input",
    )
    SIGN_IN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    LOADING_INDICATOR = (By.XPATH, "//div[contains(@class, 'VLukpV8')]")
    ERROR_MESSAGE = (
        By.XPATH,
        "//div[contains(text(), 'Пожалуйста, проверьте свой пароль')]",
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 секунд ждем по умолчанию

    def open_main_page(self):
        self.driver.get("https://store.steampowered.com/")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert "Steam" in self.driver.title

    def click_login_button(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()

    def enter_credentials(self, username, password):
        username_input = self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_FIELD)
        )
        username_input.send_keys(username)

        password_input = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        password_input.send_keys(password)

    def click_sign_in(self):
        sign_in_btn = self.wait.until(
            EC.element_to_be_clickable(self.SIGN_IN_BUTTON))
        sign_in_btn.click()

    def wait_for_loading_indicator(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOADING_INDICATOR))
            return True
        except TimeoutException:
            return False

    def wait_for_loading_to_disappear(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOADING_INDICATOR))
            return True
        except TimeoutException:
            return False

    def wait_for_error_message(self):
        try:
            error_element = self.wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            error_text = error_element.text
            return error_text
        except TimeoutException:
            return None
