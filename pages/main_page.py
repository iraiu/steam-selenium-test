from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.login_page import LoginPage



class MainPage(BasePage):

    PAGE_UNIQUE_ELEMENT = (
        By.XPATH,
        "//div[@id='global_header']//a[@data-tooltip-content='.submenu_Store']"
    )

    LOGIN_BUTTON = (By.XPATH, "//div[@id='global_action_menu']//a[contains(@href,'/login/')]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_login_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def go_to_login(self):
        self.click_login_button()
        login_page = LoginPage(self.driver)
        login_page.wait_for_open()
        return login_page