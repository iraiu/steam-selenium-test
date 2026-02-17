import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage


class TestSteamLogin:

    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def generate_random_credentials(self):
        random_num = random.randint(100, 999)
        username = f"test_user_{random_num}@test.com"
        letters = ''.join(random.choices(string.ascii_letters, k=6))
        digits = ''.join(random.choices(string.digits, k=4))
        password = letters + digits
        return username, password

    def test_login_with_invalid_credentials(self):
        self.login_page.open_main_page()
        self.login_page.click_login_button()
        username, password = self.generate_random_credentials()
        self.login_page.enter_credentials(username, password)
        self.login_page.click_sign_in()
        assert self.login_page.wait_for_loading_indicator(), \
            " Индикатор загрузки не появился после нажатия Sign In"

        assert self.login_page.wait_for_loading_to_disappear(), \
            "Индикатор загрузки не исчез"

        error_text = self.login_page.wait_for_error_message()
        assert error_text is not None, \
            "Сообщение об ошибке не появилось"

        assert "пароль" in error_text.lower() or "проверьте" in error_text.lower(), \
            f" Неожиданный текст ошибки: {error_text}"

        print("Тест успешно пройден!")
        print(f"   Использованы данные: {username} / {password}")
        print(f"   Текст ошибки: {error_text}")