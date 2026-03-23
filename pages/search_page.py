from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


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
        ".//span[contains(@class, 'title')]"
    )

    def get_current_sort_value(self):
        wait = WebDriverWait(self.driver, 10)
        sort_value_element = wait.until(
            EC.presence_of_element_located(self.SORT_BY_VALUE)
        )
        return sort_value_element.get_attribute("value")

    def set_sort_by_price_desc(self):
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
            EC.presence_of_all_elements_located(self.RESULT_ROWS)
        )

    def _sort_value_is_price_desc(self, driver):
        try:
            sort_value_element = driver.find_element(*self.SORT_BY_VALUE)
            return sort_value_element.get_attribute("value") == "Price_DESC"
        except:
            return False

    def get_first_n_prices(self, n):
        self.wait.until(
            EC.presence_of_all_elements_located(self.RESULT_ROWS)
        )

        prices = []
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                rows = self.driver.find_elements(*self.RESULT_ROWS)

                for row in rows[:n]:
                    try:
                        price_element = row.find_element(*self.ROW_PRICE)
                        price_value = price_element.get_attribute(
                            "data-price-final")

                        if price_value and price_value.isdigit():
                            price = int(price_value)
                            if price > 0:
                                prices.append(price)
                    except StaleElementReferenceException:
                        prices = []
                        break
                    except Exception:
                        continue

                if prices:
                    return prices

            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    raise
                continue

        return prices