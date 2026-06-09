import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from enmus.roles import Roles
from models.registration_user_model import RegistrationUser
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


@pytest.fixture(scope="session")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return RegistrationUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]

    )


@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session, BASE_URL)


@pytest.fixture(scope="session")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user, expected_status=201)
    return {
        "email": test_user.email,
        "password": test_user.password
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

@pytest.fixture()
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.session.close()

@pytest.fixture()
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
    [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture()
def admin_user(user_session,super_admin,creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.ADMIN.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture()
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
    [Roles.SUPER_ADMIN.value],
        new_session
    )
    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture()
def creation_user_data():
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": DataGenerator.generate_random_password(),
        "verified": True,
        "banned": False
    }

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def admin_session(session, api_manager):
    api_manager.auth_api.authenticate((SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD))
    return session

@pytest.fixture
def create_movie(admin_session, api_manager):
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

    api_manager.movies_api.delete_movie(movie["id"], expected_status=200)


@pytest.fixture
def db_session():
    session = get_db_session()
    yield session
    session.close()


@pytest.fixture
def db_helper(db_session):
    return DBHelper(db_session)

