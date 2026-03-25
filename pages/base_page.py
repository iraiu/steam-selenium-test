from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.browser_singleton import BrowserSingleton
from utils.config_reader import ConfigReader


class BasePage:
    PAGE_UNIQUE_ELEMENT = None
    DEFAULT_TIMEOUT = 10

    def __init__(self):
        self._browser = BrowserSingleton()
        self.driver = self._browser.get_driver()
        timeout = ConfigReader.get("timeout") or self.DEFAULT_TIMEOUT
        self.wait = WebDriverWait(self.driver, timeout)

    def wait_for_open(self):
        if self.PAGE_UNIQUE_ELEMENT is None:
            raise ValueError(
                f"{self.__class__.__name__}: PAGE_UNIQUE_ELEMENT is not set")

        self.wait.until(
            EC.presence_of_element_located(self.PAGE_UNIQUE_ELEMENT)
        )
