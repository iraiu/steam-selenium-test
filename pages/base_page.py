from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    PAGE_UNIQUE_ELEMENT = None

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_open(self):
        if self.PAGE_UNIQUE_ELEMENT is None:
            raise ValueError(
                f"{self.__class__.__name__}: PAGE_UNIQUE_ELEMENT is not set")

        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_UNIQUE_ELEMENT)
        )