from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.search_page import SearchPage


class MainPage(BasePage):
    PAGE_UNIQUE_ELEMENT = (By.ID, "global_header")

    SEARCH_FIELD = (
        By.XPATH,
        "//form[@role='search' and contains(@action,"
        "'store.steampowered.com/search')]//input[@name='term' and @type='text']")

    SEARCH_BUTTON = (
        By.XPATH,
        "//form[@role='search' and contains(@action,'store.steampowered.com/search')]"
        "//button[@type='submit']"
    )

    def __init__(self):
        super().__init__()  # инициализирует self.driver и self.wait

    def search(self, query: str):
        self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_FIELD)
        ).send_keys(query)

        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        ).click()

        search_page = SearchPage()
        search_page.wait_for_open()
        return search_page
