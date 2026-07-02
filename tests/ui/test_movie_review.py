import time
import allure
import pytest
from playwright.sync_api import sync_playwright

from models.login_page import CinescopeLoginPage
from models.movie_detail_page import CinescopeMovieDetailPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы фильма")
@pytest.mark.ui
class TestMovieReviewPage:
    @allure.title("Оставление отзыва под фильмом")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_leave_review(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            login_page = CinescopeLoginPage(page)
            login_page.open()
            login_page.login(registered_user.email, registered_user.password)
            page.goto("https://dev-cinescope.coconutqa.ru/movies/600")
            page.wait_for_timeout(3000)

            movie_page = CinescopeMovieDetailPage(page)
            movie_page.make_screenshot_and_attach_to_allure()

            movie_page.leave_review(rating=5, text="Отличный фильм, рекомендую!")
            movie_page.assert_review_appeared(text="Отличный фильм, рекомендую!")
            movie_page.make_screenshot_and_attach_to_allure()

            time.sleep(5)
            browser.close()
