from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver = None
            cls._instance._language = None
        return cls._instance

    def set_language(self, language):
        self._language = language

    def get_driver(self):
        if self._driver is None:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")

            if self._language:
                options.add_argument(f"--lang={self._language}")

            self._driver = webdriver.Chrome(service=service, options=options)
        return self._driver

    def quit_driver(self):
        if self._driver:
            self._driver.quit()
            self._driver = None
            self._language = None
