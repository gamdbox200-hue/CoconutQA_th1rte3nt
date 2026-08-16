import allure
import pytest

from models.ui.login_page import CinescopeLoginPage
from models.ui.movie_detail_page import CinescopeMovieDetailPage
from constants import MOVIE_URL_TEMPLATE


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы фильма")
@pytest.mark.ui
class TestMovieReviewPage:
    @allure.title("Оставление отзыва под фильмом")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_leave_review(self, registered_user, browser_page, create_movie):
        login_page = CinescopeLoginPage(browser_page)
        movie_page = CinescopeMovieDetailPage(browser_page)

        login_page.open()

        login_page.login(registered_user.email, registered_user.password)
        browser_page.goto(MOVIE_URL_TEMPLATE.format(create_movie["id"]))
        browser_page.locator("[data-qa-id='movie_rating_select']").wait_for(state="visible", timeout=15000)

        movie_page.make_screenshot_and_attach_to_allure()
        movie_page.leave_review(rating=5, text="Отличный фильм, рекомендую!")
        movie_page.assert_review_appeared(text="Отличный фильм, рекомендую!")
        movie_page.make_screenshot_and_attach_to_allure()
