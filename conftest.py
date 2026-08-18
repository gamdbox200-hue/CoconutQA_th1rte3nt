import pytest
import requests
from playwright.sync_api import sync_playwright

from constants import BASE_URL
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from entities.user import User
from enmus.roles import Roles
from models.api.registration_user_model import RegistrationUser
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from collections import namedtuple
from models.ui.login_page import CinescopeLoginPage
from models.ui.admin_page import CinescopeAdminPage

DEFAULT_UI_TIMEOUT = 30000


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session, BASE_URL)


@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)


@pytest.fixture(scope="session")
def admin_session(session, api_manager):
    api_manager.auth_api.authenticate(
        (SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD)
    )
    return session


@pytest.fixture(scope="session")
def test_user():
    password = DataGenerator.generate_random_password()
    return RegistrationUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="session")
def registered_user(api_manager, test_user):
    user_data = {k: v for k, v in test_user.model_dump().items() if v is not None}
    api_manager.auth_api.register_user(user_data, expected_status=201)
    UserCredentials = namedtuple('UserCredentials', ['email', 'password'])
    return UserCredentials(email=test_user.email, password=test_user.password)


@pytest.fixture(scope="session")
def auth_session(api_manager, registered_user):
    api_manager.auth_api.authenticate(
        (registered_user.email, registered_user.password)
    )
    return api_manager.session


@pytest.fixture()
def creation_user_data():
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": DataGenerator.generate_random_password(),
        "verified": True,
        "banned": False
    }


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
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture()
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()
    admin_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.ADMIN.value],
        new_session
    )
    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user


@pytest.fixture
def create_movie(admin_session, api_manager):
    movie_data = {
        "name": "Тестовый фильм " + DataGenerator.generate_random_name(),
        "description": "Тестовое описание",
        "price": 500,
        "location": "MSK",
        "published": True,
        "genreId": 186
    }
    response = api_manager.movies_api.create_movie(movie_data, expected_status=201)
    movie = response.json()
    yield movie
    api_manager.movies_api.delete_movie(movie["id"], expected_status=200)


@pytest.fixture(scope="session")
def existing_movie(api_manager):
    first_page = api_manager.movies_api.get_movies(expected_status=200).json()
    page_count = first_page.get("pageCount", 1)
    for page in range(1, page_count + 1):
        data = first_page if page == 1 else api_manager.movies_api.get_movies(
            params={"page": page}, expected_status=200
        ).json()
        for movie in data.get("movies", []):
            if movie.get("published") and movie.get("rating", 1) == 0:
                return movie
    raise RuntimeError("В каталоге нет опубликованных фильмов без отзывов (rating == 0)")


@pytest.fixture
def db_session():
    session = get_db_session()
    yield session
    session.close()


@pytest.fixture
def db_helper(db_session):
    return DBHelper(db_session)


@pytest.fixture(scope="session")
def playwright():
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def admin_auth(page, super_admin):
    login_page = CinescopeLoginPage(page)
    login_page.open()
    login_page.login(super_admin.email, super_admin.password)
    page.get_by_text("Профиль", exact=True).click()
    page.get_by_text("Админ панель", exact=True).wait_for(state="visible", timeout=5000)
    page.get_by_text("Админ панель", exact=True).click()
    page.wait_for_load_state("domcontentloaded")
    return CinescopeAdminPage(page)
