import pytest

class TestMoviesAPI:
    def test_get_movies_success(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200
        movies = response.json()["movies"]
        assert isinstance(movies, list)

    def test_get_movie_by_id_success(self, api_manager, admin_session, movie):
        movie_id = movie["id"]
        response = api_manager.movies_api.get_movie_by_id(movie_id)
        assert response.status_code == 200
        movie_data = response.json()
        assert movie_data["id"] == movie_id
        assert "name" in movie
        assert "price" in movie
        assert "rating" in movie
        assert "genre" in movie

    def test_get_movies_filter_by_location(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movies(params={"location": "MSK"})
        assert response.status_code == 200
        movies = response.json()["movies"]
        assert len(movies) > 0

    def test_get_movies_pagination(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movies(params={"page": 1, "pageSize": 5})
        assert response.status_code == 200
        data = response.json()
        assert len(data["movies"]) <= 5
        assert data["page"] == 1
        assert data["pageSize"] == 5

    def test_update_movie_success(self, api_manager, admin_session, movie):
        movie_id = movie["id"]
        new_price = movie["price"] + 100
        update_data = {"price": new_price}
        response = api_manager.movies_api.update_movie(movie_id,update_data)
        assert response.status_code == 200
        updated_movie = response.json()
        assert updated_movie["price"] == new_price

    def test_create_movie_missing_required_field(self, api_manager, admin_session):
        movie_data = {
            "name": "Фильм без цены",
            "description":"Описание",
            "location":"MSK",
            "published":True,
            "genreId":1
        }
        response = api_manager.movies_api.create_movie(movie_data, expected_status=400)
        assert response.status_code == 400
        assert "message" in response.json()

    def test_get_movie_nonexistent_id(self, api_manager, admin_session):
        response = api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)
        assert response.status_code == 404

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
        assert response.status_code == 400

    def test_update_movie_nonexistent_id(self, api_manager, admin_session):
        update_data = {"price":999}
        response = api_manager.movies_api.update_movie(99999999, update_data, expected_status=404)
        assert response.status_code == 404

    def test_delete_movie_success(self, api_manager, admin_session, movie):
        movie_id = movie["id"]
        response = api_manager.movies_api.delete_movie(movie_id)
        assert response.status_code == 200

        get_response = api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)
        assert get_response.status_code == 404
