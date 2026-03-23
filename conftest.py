import pytest
from enum import StrEnum
from utils.config_reader import ConfigReader
from utils.browser_singleton import BrowserSingleton


class Language(StrEnum):
    RUSSIAN = "ru"
    ENGLISH = "en"

    @property
    def locale(self):
        locales = {
            "ru": "ru-RU",
            "en": "en-US"
        }
        return locales[self.value]

    @property
    def url_param(self):
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
    BrowserSingleton.set_language(language.locale)
    driver = BrowserSingleton.get_driver()
    yield driver
    BrowserSingleton.quit_driver()


@pytest.fixture
def main_page(driver, language):
    base_url = ConfigReader.get("base_url")
    driver.get(base_url)
    from pages.main_page import MainPage
    return MainPage(driver)