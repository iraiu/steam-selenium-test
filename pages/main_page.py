from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.login_page import LoginPage

BASE_URL = "https://store.steampowered.com/"


class MainPage(BasePage):

    PAGE_UNIQUE_ELEMENT = (
        By.XPATH,
        "//div[@id='global_header']//a[@data-tooltip-content='.submenu_Store']"
    )

    LOGIN_BUTTON = (By.XPATH, "//a[contains(@href, '/login/')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        self.driver.get(BASE_URL)
        return self()

    def click_login_button(self):
        self.wait.until(EC.presence_of_all_elements_located(self.LOGIN_BUTTON))

        candidates = self.driver.find_elements(*self.LOGIN_BUTTON)
        visible = next(
            (el for el in candidates if el.is_displayed() and el.is_enabled()),
            None)

        assert visible is not None, "Login button not found (no visible clickable element matched locator)"

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", visible)
        visible.click()

    def go_to_login(self):
        self.click_login_button()
        return LoginPage(self.driver)()