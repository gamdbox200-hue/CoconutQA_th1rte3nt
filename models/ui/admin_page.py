import allure
from playwright.sync_api import Page, expect

from models.ui.base_page import BasePage


class CinescopeAdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.nav_movies = "a[href='/dashboard/movies']"
        self.nav_users = "a[href='/dashboard/users']"
        self.nav_genres = "a[href='/dashboard/genres']"

        #Навигация по странице
        self.movie_create_button = "[data-qa-id='movie_create_button']"
        self.movie_name_input = "[data-qa-id='movie_name_input']"
        self.movie_description_input = "[data-qa-id='movie_description_input']"
        self.movie_price_input = "[data-qa-id='movie_price_input']"
        self.movie_location_select = "[data-qa-id='movie_location_select']"
        self.movie_image_url_input = "[data-qa-id='movie_image_url_input']"
        self.movie_genre_select = "[data-qa-id='movie_genre_select']"
        self.movie_published_checkbox = "[data-qa-id='movie_published_checkbox']"
        self.movie_submit_button = "[data-qa-id='movie_submit_button']"

        # Форма для создания пользователя
        self.user_create_button ="[data-qa-id='user_create_button']"
        self.user_full_name_input ="[data-qa-id='user_full_name_input']"
        self.user_email_input ="[data-qa-id='user_email_input']"
        self.user_password_input = "[data-qa-id='user_password_input']"
        self.user_role_select ="[data-qa-id='user_role_select']"
        self.user_verified_checkbox ="[data-qa-id='user_verified_checkbox']"
        self.user_banned_checkbox ="[data-qa-id='user_banned_checkbox']"
        self.user_submit_button = "[data-qa-id='user_submit_button']"

        #Форма для жанра
        self.genre_create_button = "[data-qa-id='genre_create_button']"
        self.genre_create_name_input = "[data-qa-id='genre_create_name_input']"
        self.genre_create_submit_button = "[data-qa-id='genre_create_submit_button']"
        self.genre_actions_button = "[data-qa-id='genre_actions_button']"
        self.genre_delete_button = "[data-qa-id='genre_delete_button']"

    @allure.step("Перейти на страницу фильмов")
    def go_to_movies(self):
            self.click_element(self.nav_movies)
            self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Перейти на страницу пользователей")
    def go_to_users(self):
            self.click_element(self.nav_users)
            self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Перейти на страницу жанров")
    def go_to_genres(self):
        self.click_element(self.nav_genres)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Создать фильм: название='{name}'")
    def create_movie(self, name, description="Тестовое описание", price="500",
                         location="SPB", image_url="https://example.com/img.jpg", genre_index=0, published=True):
        self.click_element(self.movie_create_button)
        self.page.locator(self.movie_name_input).wait_for(state="visible", timeout=5000)
        self.enter_text_to_element(self.movie_name_input, name)
        self.enter_text_to_element(self.movie_description_input, description)
        self.page.locator(self.movie_price_input).clear()
        self.enter_text_to_element(self.movie_price_input, price)
        self.click_element(self.movie_location_select)
        self.page.get_by_text(location, exact=True).last.wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.get_by_text(location, exact=True).last)

        self.enter_text_to_element(self.movie_image_url_input, image_url)
        self.click_element(self.movie_genre_select)
        self.page.locator("[role='option']").nth(genre_index).wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.locator("[role='option']").nth(genre_index))
        if published:
            self.click_element(self.movie_published_checkbox)
        self.click_element(self.movie_submit_button)
        expect(self.page.locator(self.movie_name_input)).to_be_hidden(timeout=10000)

    @allure.step("Создать пользователя: email='{email}'")
    def create_user(self, full_name, email, password, verified=True):
        self.click_element(self.user_create_button)
        self.page.locator(self.user_full_name_input).wait_for(state="visible", timeout=5000)
        self.enter_text_to_element(self.user_full_name_input, full_name)
        self.enter_text_to_element(self.user_email_input, email)
        self.enter_text_to_element(self.user_password_input, password)
        if verified:
            self.click_element(self.user_verified_checkbox)
        self.page.get_by_text("Создания пользователя", exact=True).wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.get_by_text("Создания пользователя", exact=True))
        self.page.get_by_text("Создать", exact=True).last.wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.get_by_text("Создать", exact=True).last)
        expect(self.page.locator(self.user_full_name_input)).to_be_hidden(timeout=15000)

    @allure.step("Создать жанр: название='{name}'")
    def create_genre(self, name):
        self.click_element(self.genre_create_button)
        self.page.locator(self.genre_create_name_input).wait_for(state="visible", timeout=5000)
        self.enter_text_to_element(self.genre_create_name_input, name)
        self.click_element(self.genre_create_submit_button)
        expect(self.page.locator(self.genre_create_name_input)).to_be_hidden(timeout=10000)

    @allure.step("Удалить последний тестовый жанр (TestGenre_)")
    def delete_last_test_genre(self):
        row = self.page.locator("tr").filter(has_text="TestGenre_").last
        self.click_locator(row.locator(self.genre_actions_button))
        self.page.locator(self.genre_delete_button).wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.locator(self.genre_delete_button))
        self.page.locator("button:has-text('Удалить')").last.wait_for(state="visible", timeout=5000)
        self.click_locator(self.page.locator("button:has-text('Удалить')").last)
        self.page.wait_for_timeout(1000)

    @allure.step("Проверить, что элемент '{text}' есть в таблице")
    def assert_text_visible(self, text):
        element = self.page.get_by_text(text).first
        element.wait_for(state="visible", timeout=15000)
        assert element.is_visible(), f"Текст '{text}' не найден на странице"

    @allure.step("Проверить, что элемент '{text}' отсутствует в таблице")
    def assert_text_not_visible(self, text):
        expect(self.page.get_by_text(text)).not_to_be_visible()
