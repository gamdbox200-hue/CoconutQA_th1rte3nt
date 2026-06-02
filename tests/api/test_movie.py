import pytest
from utils.data_generator import DataGenerator


class TestMoviesAPI:
    def test_get_movies_success(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movies()
        movies = response.json()["movies"]
        assert isinstance(movies, list)

    def test_get_movie_by_id_success(self, api_manager, admin_session, create_movie):
        movie_id = create_movie["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        movie_data = response.json()
        assert movie_data["id"] == movie_id
        assert "name" in movie_data
        assert "price" in movie_data
        assert "rating" in movie_data
        assert "genre" in movie_data

    def test_movie_has_correct_location(self, api_manager, admin_session, create_movie):
        movie_data = api_manager.movies_api.get_movie_by_id(create_movie["id"]).json()
        assert movie_data["location"] == "MSK"

    def test_get_movies_pagination(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movies(params={"page": 1, "pageSize": 5})
        data = response.json()
        assert len(data["movies"]) <= 5
        assert data["page"] == 1
        assert data["pageSize"] == 5

    def test_update_movie_success(self, api_manager, admin_session, create_movie):
        movie_id = create_movie["id"]
        new_price = create_movie["price"] + 100
        update_data = {"price": new_price}
        response = api_manager.movies_api.update_movie(movie_id, update_data)
        updated_movie = response.json()
        assert updated_movie["price"] == new_price

    def test_delete_movie_success(self, api_manager, admin_session, create_movie):
        movie_data = {
            "name": "FilmForDelete " + DataGenerator.generate_random_name(),
            "description": "Test description for delete",
            "price": 300,
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = api_manager.movies_api.create_movie(movie_data, expected_status=201)
        movie_to_delete = response.json()

        api_manager.movies_api.delete_movie(movie_to_delete["id"], expected_status=200)
        api_manager.movies_api.get_movie_by_id(movie_to_delete["id"], expected_status=404)



class TestMoviesNegative:
    def test_create_movie_missing_required_field(self, api_manager, admin_session):
        movie_data = {
            "name": "Фильм без цены",
            "description": "Описание",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = api_manager.movies_api.create_movie(movie_data, expected_status=400)
        assert "message" in response.json()

    def test_get_movie_nonexistent_id(self, api_manager, admin_session):
        api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

    def test_create_movie_invalid_location(self, api_manager, admin_session):
        movie_data = {
            "name": "Bad film location",
            "price": 100,
            "description": "Описание",
            "location": "NEW-YORK",
            "published": True,
            "genreId": 1
        }
        api_manager.movies_api.create_movie(movie_data, expected_status=400)

    def test_update_movie_nonexistent_id(self, api_manager, admin_session):
        update_data = {"price": 999}
        api_manager.movies_api.update_movie(99999999, update_data, expected_status=404)