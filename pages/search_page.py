from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


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
        ".//span[@class='title']"
    )

    ROW_PRICE = (
        By.XPATH,
        ".//div[@data-price-final]"
    )

    def get_current_sort_value(self):
        sort_value_elements = self.driver.find_elements(*self.SORT_BY_VALUE)

        if not sort_value_elements:
            return None

        return sort_value_elements[0].get_attribute("value")

    def set_sort_by_price_desc(self):
        first_row_before = self.wait.until(
            EC.presence_of_element_located(self.RESULT_ROWS)
        )

        self.wait.until(
            EC.element_to_be_clickable(self.SORT_DROPDOWN_TRIGGER)
        ).click()

        price_desc_option = self.wait.until(
            EC.element_to_be_clickable(self.PRICE_DESC_OPTION)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            price_desc_option
        )

        self.wait.until(self._sort_value_is_price_desc)

        self.wait.until(
            EC.staleness_of(first_row_before)
        )

        self.wait.until(
            EC.presence_of_all_elements_located(self.RESULT_ROWS)
        )
    def get_first_n_prices(self, n):
        rows = self.wait.until(
            EC.presence_of_all_elements_located(self.RESULT_ROWS)
        )

        prices = []

        for row in rows:
            price_element = row.find_element(*self.ROW_PRICE)
            price_value = price_element.get_attribute("data-price-final")

            if not price_value:
                continue

            price = int(price_value)

            if price > 0:
                 prices.append(price)

            if len(prices) == n:
                break

        return prices

    def _sort_value_is_price_desc(self, driver):
        sort_value_elements = driver.find_elements(*self.SORT_BY_VALUE)

        if not sort_value_elements:
            return False

        return sort_value_elements[0].get_attribute("value") == "Price_DESC"