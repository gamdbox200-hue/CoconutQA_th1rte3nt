import time
import allure
import pytest
from playwright.sync_api import sync_playwright

from models.login_page import CinescopeLoginPage
from models.movie_detail_page import CinescopeMovieDetailPage


@allure.epic("Тестирование UI")
@allure.feature("Негативные тесты")
@pytest.mark.ui
class TestNegativeUI:

    @allure.title("Отправка отзыва с пустым текстом")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_leave_review_empty_text(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            login_page = CinescopeLoginPage(page)
            login_page.open()
            login_page.login(registered_user.email, registered_user.password)
            page.wait_for_timeout(3000)
            page.goto("https://dev-cinescope.coconutqa.ru/movies/57741")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)

            movie_page = CinescopeMovieDetailPage(page)
            movie_page.make_screenshot_and_attach_to_allure()
            movie_page.leave_review(rating=5, text="")
            movie_page.assert_review_not_appeared("")

            time.sleep(3)
            browser.close()

    @allure.title("Отправка отзыва с текстом менее 5 символов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_leave_review_short_text(self, registered_user):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            login_page = CinescopeLoginPage(page)
            login_page.open()
            login_page.login(registered_user.email, registered_user.password)
            page.wait_for_timeout(3000)
            page.goto("https://dev-cinescope.coconutqa.ru/movies/57741")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)

            movie_page = CinescopeMovieDetailPage(page)
            movie_page.make_screenshot_and_attach_to_allure()
            movie_page.leave_review(rating=5, text="Hi")
            movie_page.assert_review_not_appeared("Hi")

            time.sleep(3)
            browser.close()
