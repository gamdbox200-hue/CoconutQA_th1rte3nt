import allure
import pytest

from models.ui.login_page import CinescopeLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user, page):
        login_page = CinescopeLoginPage(page)

        login_page.open()
        login_page.login(registered_user.email, registered_user.password)

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
