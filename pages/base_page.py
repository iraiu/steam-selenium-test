from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    PAGE_UNIQUE_ELEMENT = None

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def __call__(self):
        assert self.PAGE_UNIQUE_ELEMENT, (
            f"{self.__class__.__name__} has no PAGE_UNIQUE_ELEMENT"
        )

        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_UNIQUE_ELEMENT)
        )

        return self