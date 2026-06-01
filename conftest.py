import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager


@pytest.fixture(scope="session")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session, BASE_URL)


@pytest.fixture(scope="session")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user, expected_status=201)
    return {
        "email": test_user["email"],
        "password": test_user["password"]
    }

@pytest.fixture(scope="session")
def auth_session(api_manager, registered_user):
    api_manager.auth_api.authenticate(
        (registered_user["email"], registered_user["password"])
    )
    return api_manager.session

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

ADMIN_CREDS = ("api1@gmail.com", "asdqwe123Q")

@pytest.fixture(scope="session")
def admin_session(session,api_manager):
    api_manager.auth_api.authenticate(ADMIN_CREDS)
    return session

@pytest.fixture
def movie(admin_session, api_manager):  # scope="function" — новый фильм для каждого теста
    movie_data = {
        "name": "Тестовый фильм " + DataGenerator.generate_random_name(),
        "description": "Тестовое описание",
        "price": 500,
        "location": "MSK",
        "published": True,
        "genreId": 1
    }
    response = api_manager.movies_api.create_movie(movie_data, expected_status=201)
    movie = response.json()
    yield movie