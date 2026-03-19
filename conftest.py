import pytest

from pages.main_page import MainPage
from utils.browser_singleton import BrowserSingleton
from utils.config_reader import ConfigReader


def pytest_addoption(parser):
    parser.addoption(
        "--lang",
        action="store",
        default="ru",
        help="Language for tests: ru or en"
    )


@pytest.fixture()
def driver():
    browser = BrowserSingleton()
    driver = browser.get_driver()
    yield driver
    browser.quit_driver()


@pytest.fixture
def language(request):
    return request.config.getoption("--lang")


@pytest.fixture
def main_page(driver, language):
    base_url = ConfigReader.get("base_url")
    if language == "ru":
        driver.get(f"{base_url}?l=russian")
    elif language == "en":
        driver.get(f"{base_url}?l=english")
    else:
        raise ValueError(f"Unsupported language: {language}")

    page = MainPage(driver)
    page.wait_for_open()
    return page