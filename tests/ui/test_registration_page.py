import allure
import pytest

from models.ui.register_page import CinescopeRegisterPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, browser_page):
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopeRegisterPage(browser_page)

        register_page.open()
        register_page.register(f"PlaywrightTest {random_name}", random_email, random_password, random_password)

        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()
