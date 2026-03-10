from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.login_page import LoginPage



class MainPage(BasePage):

    PAGE_UNIQUE_ELEMENT = (By.ID, "global_header")
    LOGIN_BUTTON = (By.XPATH, "//div[@id='global_action_menu']//a[contains(@href,'/login/')]")

    def click_login_button(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def go_to_login(self):
        self.click_login_button()
        login_page = LoginPage(self.driver)
        login_page.wait_for_open()
        return login_page