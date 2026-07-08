import allure
import pytest

from models.ui.admin_page import CinescopeAdminPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI админ-панели")
@allure.feature("Управление фильмами")
@pytest.mark.ui
class TestAdminMovies:
    @allure.title("Успешное создание фильма через админку")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_admin_create_movie(self, admin_auth):
        admin = CinescopeAdminPage(admin_auth)
        movie_name = "UI Test Film " + DataGenerator.generate_random_name()
        admin.go_to_movies()
        admin.create_movie(name=movie_name, price="500", location="SPB")
        admin.assert_text_visible(movie_name)

    @allure.title("Нельзя создать фильм с пустым названием")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_admin_create_movie_empty_name(self, admin_auth):
        admin = CinescopeAdminPage(admin_auth)
        admin.go_to_movies()
        admin.click_element(admin.movie_create_button)
        admin.page.wait_for_timeout(1000)
        admin.enter_text_to_element(admin.movie_description_input, "Тест")
        admin.enter_text_to_element(admin.movie_price_input, "100")
        admin.click_element(admin.movie_submit_button)
        admin.page.wait_for_timeout(1000)
        # Модалка должна остаться открытой
        assert admin.page.locator(admin.movie_name_input).is_visible(), (
            "Модалка закрылась — фильм создался с пустым названием"
        )

@allure.epic("Тестирование UI админ-панели")
@allure.feature("Управление пользователями")
@pytest.mark.ui
class TestAdminUsers:
    @allure.title("Успешное создание пользователя через админку")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_admin_create_user(self, admin_auth):
        admin = CinescopeAdminPage(admin_auth)
        user_email = DataGenerator.generate_random_email()
        admin.go_to_users()
        admin.create_user(
            full_name="Test UI User",
            email=user_email,
            password="TestPass12345!"
        )
        admin.assert_text_visible(user_email)

@allure.epic("Тестирование UI админ-панели")
@allure.feature("Управление жанрами")
@pytest.mark.ui
class TestAdminGenres:
    @allure.title("Успешное создание и удаление жанра")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_admin_create_and_delete_genre(self, admin_auth):
        admin = CinescopeAdminPage(admin_auth)
        genre_name = "TestGenre_" + DataGenerator.generate_random_name()
        admin.go_to_genres()
        admin.create_genre(genre_name)
        admin.assert_text_visible(genre_name)
        admin.delete_last_test_genre()
        admin.assert_text_not_visible(genre_name)