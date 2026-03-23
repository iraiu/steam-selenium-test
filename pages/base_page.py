from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader

class BasePage:
    PAGE_UNIQUE_ELEMENT = None

    def __init__(self, driver):
        self.driver = driver
        timeout = ConfigReader.get("timeout")

        if timeout is None:
            timeout = 10

        self.wait = WebDriverWait(driver, timeout)

    def wait_for_open(self):
        if self.PAGE_UNIQUE_ELEMENT is None:
            raise ValueError(
                f"{self.__class__.__name__}: PAGE_UNIQUE_ELEMENT is not set")

        self.wait.until(
            EC.presence_of_all_elements_located(self.PAGE_UNIQUE_ELEMENT)
        )