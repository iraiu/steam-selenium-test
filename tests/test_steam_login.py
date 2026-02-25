import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages.main_page import MainPage

fake = Faker()

def generate_random_credentials():
    return fake.email(), fake.password(length=10)

def test_login_with_invalid_credentials(main_page):
    main_page.open()
    login_page = main_page.go_to_login()

    username, password = generate_random_credentials()
    login_page.enter_credentials(username, password)
    login_page.click_sign_in()

    login_page.wait_for_loading_to_disappear()

    error_text = login_page.wait_for_error_message()
    assert error_text is not None

    expected_text = "Пожалуйста, проверьте свой пароль и имя аккаунта и попробуйте снова."
    assert error_text == expected_text