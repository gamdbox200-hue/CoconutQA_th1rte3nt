import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester


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
def registered_user(requester, test_user):
    response = requester.send_request(
        "POST", REGISTER_ENDPOINT, data=test_user, expected_status=201
    )
    # Возвращаем только то, что нужно для логина
    return {
        "email": test_user["email"],
        "password": test_user["password"]
    }


@pytest.fixture(scope="session")
def auth_session(requester, registered_user):
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = requester.send_request(
        "POST", LOGIN_ENDPOINT, data=login_data, expected_status=200
    )
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"

    session = requests.Session()
    session.headers.update(requester.headers)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session