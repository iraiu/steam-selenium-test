from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.search_page import SearchPage


class MainPage(BasePage):
    PAGE_UNIQUE_ELEMENT = (By.ID, "global_header")

    SEARCH_FIELD = (
        By.XPATH,
        "//form[@role='search' and contains(@action,'store.steampowered.com/search')]//input[@name='term' and @type='text']"
    )

    ADVANCED_SEARCH_BUTTON = (
        By.XPATH,
        "//a[contains(@href,'/search/?term=') and contains(@href,'advancedsearch')]"
    )

    def open_advanced_search(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_FIELD)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(self.ADVANCED_SEARCH_BUTTON)
        ).click()

        search_page = SearchPage(self.driver)
        search_page.wait_for_open()
        return search_page