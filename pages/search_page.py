from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException


class SearchPage(BasePage):
    PAGE_UNIQUE_ELEMENT = (By.ID, "search_results")
    SORT_DROPDOWN_TRIGGER = (By.ID, "sort_by_trigger")
    PRICE_DESC_OPTION = (By.ID, "Price_DESC")
    SORT_BY_VALUE = (By.ID, "sort_by")
    RESULTS_LOADING = (By.ID, "search_results_loading")
    RESULT_ROWS = (
        By.XPATH,
        "//*[@id='search_resultsRows']/a[contains(@class,'search_result_row')]"
    )
    ROW_TITLE = (
        By.XPATH,
        ".//span[contains(@class, 'title')]"
    )
    ROW_PRICE = (
        By.XPATH,
        ".//div[@data-price-final]"
    )

    def __init__(self):
        super().__init__()

    def get_current_sort_value(self):
        sort_value_elements = self.wait.until(
            EC.presence_of_all_elements_located(self.SORT_BY_VALUE)
        )
        return sort_value_elements[0].get_attribute("value")

    def set_sort_by_price_desc(self):
        self.wait.until(
            EC.element_to_be_clickable(self.SORT_DROPDOWN_TRIGGER)
        ).click()

        price_desc_option = self.wait.until(
            EC.element_to_be_clickable(self.PRICE_DESC_OPTION)
        )
        price_desc_option.click()

        self.wait.until(self._sort_value_is_price_desc())

        try:
            self.wait.until(
                EC.visibility_of_element_located(self.RESULTS_LOADING)
            )
        except TimeoutException:
            pass

        self.wait.until(
            EC.invisibility_of_element_located(self.RESULTS_LOADING)
        )

        self.wait.until(
            EC.presence_of_all_elements_located(self.RESULT_ROWS)
        )

    def _sort_value_is_price_desc(self):
        def predicate(driver):
            sort_value_elements = driver.find_elements(*self.SORT_BY_VALUE)
            if not sort_value_elements:
                return False
            return sort_value_elements[0].get_attribute(
                "value") == "Price_DESC"

        return predicate

    def get_first_n_prices(self, n):
        def prices_loaded(driver):
            rows = driver.find_elements(*self.RESULT_ROWS)
            if len(rows) < n:
                return None

            prices = []
            for row in rows:
                price_elements = row.find_elements(*self.ROW_PRICE)
                if not price_elements:
                    continue
                price_value = price_elements[0].get_attribute(
                    "data-price-final")
                if not price_value or not price_value.isdigit():
                    continue
                price = int(price_value)
                if price > 0:
                    prices.append(price)
                if len(prices) == n:
                    return prices
            return None

        return self.wait.until(prices_loaded)
