import pytest

from pages.main_page import MainPage
from utils.browser_singleton import BrowserSingleton

BASE_URL = "https://store.steampowered.com/"


def pytest_addoption(parser):
    parser.addoption(
        "--lang",
        action="store",
        default="ru",
        help="Language for tests: ru or en"
    )


@pytest.fixture(scope="session")
def driver():
    driver = BrowserSingleton.get_driver()
    yield driver
    BrowserSingleton.quit_driver()


@pytest.fixture
def language(request):
    return request.config.getoption("--lang")


@pytest.fixture
def main_page(driver, language):
    if language == "ru":
        driver.get(f"{BASE_URL}?l=russian")
    elif language == "en":
        driver.get(f"{BASE_URL}?l=english")
    else:
        raise ValueError(f"Unsupported language: {language}")

    page = MainPage(driver)
    page.wait_for_open()
    return page