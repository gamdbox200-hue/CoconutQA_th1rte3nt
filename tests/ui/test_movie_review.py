import time
import allure
import pytest
import requests
from playwright.sync_api import sync_playwright

from models.page_object_models import CinescopeLoginPage, CinescopeMovieDetailPage


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

            with allure.step("Логин в систему"):
                login_page = CinescopeLoginPage(page)
                login_page.open()
                login_page.login(registered_user.email, registered_user.password)
                page.wait_for_load_state("networkidle")

            with allure.step("Переход на страницу фильма"):
                movie_page = CinescopeMovieDetailPage(page)
                movie_page.open(movie_id=56964)

            with allure.step("Скриншот страницы фильма"):
                movie_page.make_screenshot_and_attach_to_allure()

            with allure.step("Оставить отзыв"):
                movie_page.leave_review(rating=5, text="Отличный фильм, рекомендую!")

            with allure.step("Проверить что отзыв появился"):
                movie_page.assert_review_appeared(text="Отличный фильм, рекомендую!")

            movie_page.make_screenshot_and_attach_to_allure()

            time.sleep(5)
            browser.close()
