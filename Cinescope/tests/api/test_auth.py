import pytest
import requests
from Cinescope.constants import BASE_URL,HEADERS, REGISTER_ENDPOINT

class TestAuthAPI:
    def test_register_user(self, test_user):
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        response = requests.post(register_url, json=test_user, headers=HEADERS)

        print(f"Response status:{response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"


