import pytest
import allure
from pytest_check import check
from utils.data_generator import DataGenerator
from models.movie_model import MovieModel, MoviesListResponse


@allure.feature("Movies API")
@allure.story("Get Movies")
class TestMoviesAPI:

    @allure.title("Получение списка фильмов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "api")
    def test_get_movies_success(self, api_manager, admin_session):
        with allure.step("Отправить GET-запрос на /movies"):
            response = api_manager.movies_api.get_movies()
            movies = response.json()["movies"]
        with allure.step("Проверить, что movies — это список"):
            check.is_instance(movies, list, "movies должен быть списком")

    @allure.title("Получение фильма по ID — валидация через Pydantic")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movie_by_id_success(self, api_manager, admin_session, create_movie):
        movie_id = create_movie["id"]
        with allure.step(f"Отправить GET-запрос на /movies/{movie_id}"):
            response = api_manager.movies_api.get_movie_by_id(movie_id)
            movie_data = response.json()

        with allure.step("Проверить id фильма"):
            check.equal(movie_data["id"], movie_id, f"Ожидался id {movie_id}, получен {movie_data['id']}")
        with allure.step("Проверить наличие поля name"):
            check.is_in("name", movie_data, "Поле name отсутствует в ответе")
        with allure.step("Проверить наличие поля price"):
            check.is_in("price", movie_data, "Поле price отсутствует в ответе")
        with allure.step("Проверить наличие поля rating"):
            check.is_in("rating", movie_data, "Поле rating отсутствует в ответе")
        with allure.step("Проверить наличие поля genre"):
            check.is_in("genre", movie_data, "Поле genre отсутствует в ответе")

        with allure.step("Валидация схемы ответа через Pydantic MovieModel"):
            validated = MovieModel.model_validate(movie_data)
            check.equal(validated.id, movie_id)
            check.is_true(validated.name, "Имя фильма не должно быть пустым")
            check.is_in(validated.location, ("MSK", "SPB"), "Локация должна быть MSK или SPB")

    @allure.title("Проверка локации созданного фильма")
    @allure.severity(allure.severity_level.NORMAL)
    def test_movie_has_correct_location(self, api_manager, admin_session, create_movie):
        with allure.step(f"Получить данные фильма id={create_movie['id']}"):
            movie_data = api_manager.movies_api.get_movie_by_id(create_movie["id"]).json()
        with allure.step("Проверить, что location = 'MSK'"):
            check.equal(movie_data["location"], "MSK")

    @allure.title("Пагинация списка фильмов (page=1, pageSize=5) — валидация через Pydantic")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_pagination(self, api_manager, admin_session):
        with allure.step("Отправить GET-запрос с параметрами page=1, pageSize=5"):
            response = api_manager.movies_api.get_movies(params={"page": 1, "pageSize": 5})
            data = response.json()

        with allure.step("Проверить, что количество фильмов <= 5"):
            check.less_equal(len(data["movies"]), 5,
                             f"Ожидалось не более 5 фильмов, получено {len(data['movies'])}")
        with allure.step("Проверить page=1"):
            check.equal(data["page"], 1, f"Ожидалась страница 1, получена {data['page']}")
        with allure.step("Проверить pageSize=5"):
            check.equal(data["pageSize"], 5, f"Ожидался pageSize 5, получен {data['pageSize']}")

        with allure.step("Валидация схемы списка фильмов через Pydantic MoviesListResponse"):
            validated = MoviesListResponse.model_validate(data)
            check.equal(validated.page, 1)
            check.equal(validated.pageSize, 5)
            check.is_instance(validated.movies, list)
            if validated.movies:
                check.is_instance(validated.movies[0], MovieModel)

    @allure.story("Update Movie")
    @allure.title("Обновление цены фильма")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_movie_success(self, api_manager, admin_session, create_movie):
        movie_id = create_movie["id"]
        new_price = create_movie["price"] + 100
        update_data = {"price": new_price}

        with allure.step(f"Отправить PUT-запрос на /movies/{movie_id} с price={new_price}"):
            response = api_manager.movies_api.update_movie(movie_id, update_data)
            updated_movie = response.json()

        with allure.step("Проверить, что цена обновлена"):
            check.equal(updated_movie["price"], new_price,
                        f"Ожидалась цена {new_price}, получена {updated_movie['price']}")

    @allure.story("Delete Movie")
    @allure.title("Удаление фильма по полному циклу: создание → удаление → проверка 404")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movie_success(self, api_manager, admin_session):
        with allure.step("Создать тестовый фильм для удаления"):
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

        with allure.step(f"Удалить фильм id={movie_to_delete['id']}"):
            api_manager.movies_api.delete_movie(movie_to_delete["id"], expected_status=200)

        with allure.step("Проверить, что фильм недоступен (404)"):
            api_manager.movies_api.get_movie_by_id(movie_to_delete["id"], expected_status=404)


    @allure.story("Filter Movies")
    @allure.title("Фильтрация фильмов по цене (min={min_price}, max={max_price})")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("min_price, max_price" , [
        (1, 1000),
        (100, 500),
        (500, 1000),
        (1, 50),
    ])
    def test_movies_filter_by_price(self, api_manager, admin_session, min_price, max_price):
        with allure.step(f"Запросить фильмы с minPrice={min_price}, maxPrice={max_price}"):
            params = {"minPrice": min_price, "maxPrice": max_price}
            movies = api_manager.movies_api.get_movies(params=params).json()["movies"]

        with allure.step(f"Проверить, что каждый фильм в диапазоне [{min_price}, {max_price}]"):
            for movie in movies:
                check.is_true(
                    min_price <= movie["price"] <= max_price,
                    f"Фильм '{movie.get('name', movie['id'])}': цена {movie['price']} вне диапазона [{min_price}, {max_price}]"
                )

    @allure.story("Filter Movies")
    @allure.title("Фильтрация фильмов по локации ({location})")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("location", ["MSK", "SPB"])
    def test_movie_filter_by_location(self, api_manager, admin_session, location):
        with allure.step(f"Запросить все фильмы"):
            movies = api_manager.movies_api.get_movies().json()["movies"]

        with allure.step(f"Проверить, что каждый фильм имеет допустимую локацию"):
            for movie in movies:
                check.is_in(
                    movie["location"], ("MSK", "SPB"),
                    f"Фильм '{movie.get('name', movie['id'])}': локация {movie['location']} недопустима"
                )

    @allure.story("Filter Movies")
    @allure.title("Фильтрация фильмов по жанру (genreId={genre_id})")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("genre_id", [1, 2, 3, 4, 5])
    def test_movies_filter_by_genre(self, api_manager, admin_session, genre_id):
        with allure.step(f"Запросить фильмы с genreId={genre_id}"):
            params = {"genreId": genre_id}
            movies = api_manager.movies_api.get_movies(params=params).json()["movies"]

        with allure.step(f"Проверить, что каждый фильм имеет genreId={genre_id}"):
            for movie in movies:
                check.equal(
                    movie["genreId"], genre_id,
                    f"Фильм '{movie.get('name', movie['id'])}': ожидался genreId={genre_id}, получен {movie['genreId']}"
                )


@allure.feature("Movies API")
@allure.story("Negative Tests")
class TestMoviesNegative:

    @allure.title("Создание фильма без обязательного поля price")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_missing_required_field(self, api_manager, admin_session):
        with allure.step("Создать фильм без поля price"):
            movie_data = {
                "name": "Фильм без цены",
                "description": "Описание",
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            response = api_manager.movies_api.create_movie(movie_data, expected_status=400)
            response_data = response.json()

        with allure.step("Проверить, что в ответе есть message"):
            check.is_in("message", response_data, "Поле message отсутствует в ответе")
        with allure.step("Проверить, что сообщение содержит упоминание price"):
            check.is_true(
                any("price" in msg for msg in response_data["message"]),
                f"Сообщение об ошибке не содержит 'price': {response_data['message']}"
            )

    @allure.title("Получение несуществующего фильма — ожидается 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movie_nonexistent_id(self, api_manager, admin_session):
        with allure.step("Запросить фильм с id=999999999"):
            api_manager.movies_api.get_movie_by_id(999999999, expected_status=404)

    @allure.title("Создание фильма с недопустимой локацией — ожидается 400")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_movie_invalid_location(self, api_manager, admin_session):
        with allure.step("Создать фильм с локацией 'NEW-YORK'"):
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

        with allure.step("Проверить, что в ответе есть message"):
            check.is_in("message", response_data, "Поле message отсутствует в ответе")
        with allure.step("Проверить, что сообщение содержит упоминание location"):
            check.is_true(
                any("location" in msg for msg in response_data["message"]),
                f"Сообщение об ошибке не содержит 'location': {response_data['message']}"
            )

    @allure.title("Обновление несуществующего фильма — ожидается 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_movie_nonexistent_id(self, api_manager, admin_session):
        with allure.step("Обновить фильм с id=99999999"):
            update_data = {"price": 999}
            api_manager.movies_api.update_movie(99999999, update_data, expected_status=404)

    @allure.title("Пользователь без прав не может создать фильм — ожидается 403")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "api")
    @pytest.mark.slow
    def test_user_cannot_create_movie(self, common_user):
        with allure.step("Попытаться создать фильм от имени обычного пользователя"):
            movie_data = {
                "name": "Фильм от юзера",
                "description": "Описание",
                "price": 500,
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            common_user.api.movies_api.create_movie(movie_data, expected_status=403)

    @allure.title("Проверка прав на удаление фильма: common_user(403), admin_user(403), super_admin(200)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "api")
    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture_name, expected_status", [
        ("common_user", 403),
        ("admin_user", 403),
        ("super_admin", 200),
    ])
    def test_delete_movie_by_role(self, request, api_manager, admin_session, user_fixture_name, expected_status):
        with allure.step("Создать тестовый фильм для удаления"):
            movie_data = {
                "name": "FilmForRoleDelete " + DataGenerator.generate_random_name(),
                "description": "Tested",
                "price": 300,
                "location": "MSK",
                "published": True,
                "genreId": 1
            }
            movie = api_manager.movies_api.create_movie(movie_data, expected_status=201).json()

        with allure.step(f"Попытаться удалить фильм от имени {user_fixture_name} (ожидается {expected_status})"):
            user = request.getfixturevalue(user_fixture_name)
            user.api.movies_api.delete_movie(movie["id"], expected_status=expected_status)

        if expected_status == 200:
            with allure.step("Проверить, что фильм действительно удалён (404)"):
                api_manager.movies_api.get_movie_by_id(movie["id"], expected_status=404)