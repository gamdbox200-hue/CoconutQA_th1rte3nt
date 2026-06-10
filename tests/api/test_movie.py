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

    def test_delete_movie_success(self, api_manager, admin_session):
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


    @pytest.mark.parametrize("min_price, max_price" , [
        (1, 1000),
        (100, 500),
        (500, 1000),
        (1, 50),
    ])
    def test_movies_filter_by_price(self, api_manager, admin_session, min_price, max_price):
        params = {"minPrice": min_price, "maxPrice": max_price}
        movies = api_manager.movies_api.get_movies(params=params).json()["movies"]
        for movie in movies:
            assert min_price <= movie["price"] <= max_price

    @pytest.mark.parametrize("location", ["MSK", "SPB"])
    def test_movie_filter_by_location(self, api_manager, admin_session, location):
        movies = api_manager.movies_api.get_movies().json()["movies"]
        for movie in movies:
            assert movie["location"] in ("MSK", "SPB")

    @pytest.mark.parametrize("genre_id", [1, 2, 3, 4, 5])
    def test_movies_filter_by_genre(self, api_manager, admin_session, genre_id):
        params = {"genreId": genre_id}
        movies = api_manager.movies_api.get_movies(params=params).json()["movies"]
        for movie in movies:
            assert movie["genreId"] == genre_id


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
        response_data = response.json()
        assert "message" in response_data
        assert any("price" in msg for msg in response_data["message"])

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
        response = api_manager.movies_api.create_movie(movie_data, expected_status=400)
        response_data = response.json()
        assert "message" in response_data
        assert any("location" in msg for msg in response_data["message"])

    def test_update_movie_nonexistent_id(self, api_manager, admin_session):
        update_data = {"price": 999}
        api_manager.movies_api.update_movie(99999999, update_data, expected_status=404)

    @pytest.mark.slow
    def test_user_cannot_create_movie(self, common_user):
        movie_data = {
            "name": "Фильм от юзера",
            "description": "Описание",
            "price": 500,
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        response = common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture_name, expected_status", [
        ("common_user", 403),
        ("admin_user", 403),
        ("super_admin", 200),
    ])
    def test_delete_movie_by_role(self, request, api_manager, admin_session, user_fixture_name, expected_status):
        movie_data = {
            "name": "FilmForRoleDelete " + DataGenerator.generate_random_name(),
            "description": "Tested",
            "price": 300,
            "location": "MSK",
            "published": True,
            "genreId": 1
        }
        movie = api_manager.movies_api.create_movie(movie_data, expected_status=201).json()
        user = request.getfixturevalue(user_fixture_name)
        user.api.movies_api.delete_movie(movie["id"], expected_status=expected_status)
        if expected_status == 200:
            api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)