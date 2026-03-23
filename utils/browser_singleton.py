from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrowserSingleton:
    _driver = None
    _language = None

    @classmethod
    def set_language(cls, language):
        cls._language = language

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")

            if cls._language:
                options.add_argument(f"--lang={cls._language}")

            cls._driver = webdriver.Chrome(service=service, options=options)
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            cls._language = None