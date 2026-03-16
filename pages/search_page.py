from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import BasePage


class SearchPage(BasePage):
    PAGE_UNIQUE_ELEMENT = (By.ID, "search_results")

    SEARCH_FIELD = (By.ID, "term")
    REAL_TERM_FIELD = (By.ID, "realterm")

    SEARCH_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'searchbar_left')]//button[@type='submit']"
    )

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
        ".//div[contains(@class,'search_price_discount_combined')]"
    )

    def search_for_game(self, game_name):
        search_field = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_FIELD)
        )
        search_field.click()

        self.driver.execute_script(
            """
            const visible = document.getElementById('term');
            const hidden = document.getElementById('realterm');

            visible.value = arguments[0];
            hidden.value = arguments[0];

            visible.dispatchEvent(new Event('input', { bubbles: true }));
            visible.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            game_name
        )

        self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(self.RESULTS_LOADING)
        )

        # Берём самое длинное слово запроса, чтобы не ловить мусор вроде "the"
        query_token = max(game_name.lower().split(), key=len)

        self.wait.until(
            lambda driver: any(
                query_token in row.find_element(*self.ROW_TITLE).text.lower()
                for row in driver.find_elements(*self.RESULT_ROWS)[:20]
            )
        )

    def set_sort_by_price_desc(self):
        first_row_before_sort = self.wait.until(
            EC.presence_of_element_located(self.RESULT_ROWS)
        )

        self.wait.until(
            EC.element_to_be_clickable(self.SORT_DROPDOWN_TRIGGER)
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(self.PRICE_DESC_OPTION)
        ).click()

        self.wait.until(
            lambda driver: driver.find_element(*self.SORT_BY_VALUE).get_attribute("value") == "Price_DESC"
        )

        self.wait.until(
            EC.staleness_of(first_row_before_sort)
        )

        self.wait.until(
            EC.invisibility_of_element_located(self.RESULTS_LOADING)
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
            try:
                price_element = row.find_element(*self.ROW_PRICE)
                price_value = price_element.get_attribute("data-price-final")

                if price_value is None or price_value == "":
                    continue

                price = int(price_value)

                if price > 0:
                    prices.append(price)

            except NoSuchElementException:
                continue

            if len(prices) == n:
                break

        return prices

    @staticmethod
    def are_prices_sorted_desc(prices):
        return prices == sorted(prices, reverse=True)