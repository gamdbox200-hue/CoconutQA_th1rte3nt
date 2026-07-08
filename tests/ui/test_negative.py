import allure
import pytest

from models.ui.login_page import CinescopeLoginPage
from models.ui.movie_detail_page import CinescopeMovieDetailPage
from constants import MOVIE_URL_TEMPLATE


@allure.epic("Тестирование UI")
@allure.feature("Негативные тесты")
@pytest.mark.ui
class TestNegativeUI:

    @allure.title("Отправка отзыва с некорректным текстом")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("review_text", [
        "",
        "Hi",
    ])
    def test_leave_review_invalid_text(self, registered_user, browser_page, review_text):
        login_page = CinescopeLoginPage(browser_page)
        movie_page = CinescopeMovieDetailPage(browser_page)

        login_page.open()
        login_page.login(registered_user.email, registered_user.password)
        browser_page.goto(MOVIE_URL_TEMPLATE.format(59920))
        browser_page.wait_for_timeout(3000)

        movie_page.make_screenshot_and_attach_to_allure()
        movie_page.leave_review(rating=5, text=review_text)
        movie_page.assert_review_form_not_submitted(expected_text=review_text)
        movie_page.make_screenshot_and_attach_to_allure()
