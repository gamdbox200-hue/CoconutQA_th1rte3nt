import pytest
from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator


class TestAuthAPI:
    def test_register_user(self, api_manager):
        password = DataGenerator.generate_random_password()
        user_data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"]
        }

        response = api_manager.auth_api.register_user(user_data, expected_status=201)

        response_data = response.json()
        assert response_data["email"] == user_data["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_login_success(self, registered_user, api_manager):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(payload, expected_status=200)

        response_data = response.json()
        assert "accessToken" in response_data, "accessToken отсутствует в ответе"
        assert response_data["accessToken"], "accessToken не должен быть пустым"
        assert "user" in response_data, "Объект user отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], (
            f"Email не совпадает: ожидался {registered_user['email']}, "
            f"получен {response_data['user']['email']}"
        )

    def test_login_invalid_password(self, registered_user, api_manager):
        payload = {
            "email": registered_user["email"],
            "password": "WrongPassword123123"
        }

        response = api_manager.auth_api.login_user(payload, expected_status=401)


        response_data = response.json()
        assert "message" in response_data, "Нет поля message в ответе"
        assert response_data["message"], "Сообщение об ошибке пустое"

    def test_login_nonexistent_email(self, api_manager):
        payload = {
            "email": DataGenerator.generate_random_email(),
            "password": "Somepass123123"
        }

        response = api_manager.auth_api.login_user(payload, expected_status=401)

        response_data = response.json()
        assert "message" in response_data, "Нет поля message в ответе"
        assert response_data["message"], "Сообщение об ошибке пустое"

    def test_login_empty_body(self, api_manager):
        response = api_manager.auth_api.login_user({}, expected_status=401)

        response_data = response.json()
        assert "message" in response_data, "Нет поля message в ответе"
        assert response_data["message"], "Сообщение об ошибке пустое"