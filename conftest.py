import pytest
from enum import StrEnum
from utils.config_reader import ConfigReader
from utils.browser_singleton import BrowserSingleton
from pages.main_page import MainPage


class Language(StrEnum):
    RUSSIAN = "ru"
    ENGLISH = "en"

    @property
    def locale(self):
        return self.value


def pytest_addoption(parser):
    parser.addoption(
        "--lang",
        action="store",
        default="ru",
        choices=["ru", "en"],
        help="Language for tests: ru or en"
    )


@pytest.fixture
def language(request):
    lang_param = request.config.getoption("--lang")
    return Language(lang_param)


@pytest.fixture
def driver(language):
    browser = BrowserSingleton()  # получаем экземпляр синглтона
    browser.set_language(language.locale)
    driver = browser.get_driver()
    yield driver
    browser.quit_driver()


@pytest.fixture
def main_page(driver):
    base_url = ConfigReader.get("base_url")
    driver.get(base_url)
    page = MainPage()
    page.wait_for_open()
    return page
