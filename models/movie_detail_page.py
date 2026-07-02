import allure
from playwright.sync_api import Page

from models.base_page import BasePage


class CinescopeMovieDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.review_textarea = "[data-qa-id='movie_review_input']"
        self.rating_combobox = "[data-qa-id='movie_rating_select']"
        self.submit_review_button = "[data-qa-id='movie_review_submit_button']"

    def open(self, movie_id: int):
        self.open_url(f"{self.home_url}movies/{movie_id}")

    @allure.step("Нажать на фильм в списке")
    def click_first_movie(self):
        self.page.locator("a[href*='/movies/']").nth(1).click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Оставить отзыв: оценка={rating}, текст='{text}'")
    def leave_review(self, rating: int, text: str):
        self.page.locator(self.rating_combobox).click()
        self.page.get_by_text(str(rating), exact=True).last.click()
        self.enter_text_to_element(self.review_textarea, text)
        self.click_element(self.submit_review_button)

    @allure.step("Проверить что отзыв с текстом '{text}' появился")
    def assert_review_appeared(self, text: str):
        review = self.page.get_by_text(text).first
        review.wait_for(state="visible")
        assert review.is_visible(), f"Отзыв с текстом '{text}' не появился"

    @allure.step("Проверить что форма не отправилась")
    def assert_review_not_appeared(self, expected_text: str):
        self.page.wait_for_timeout(1000)
        textarea_value = self.page.locator(self.review_textarea).input_value()
        assert textarea_value == expected_text, f"Форма отправилась — поле очистилось, ожидалось '{expected_text}'"
