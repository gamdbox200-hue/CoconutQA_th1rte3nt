from conftest import super_admin, creation_user_data
from api.api_manager import ApiManager
from models.registration_user_model import RegisterUserResponse

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = RegisterUserResponse.model_validate(
            super_admin.api.user_api.create_user(creation_user_data).json()
        )
        assert response.id, "ID должен быть не пустым"
        assert response.email == creation_user_data["email"]
        assert response.fullName == creation_user_data["fullName"]
        assert response.roles == ["USER"]
        assert response.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created = RegisterUserResponse.model_validate(
            super_admin.api.user_api.create_user(creation_user_data).json()
        )
        by_id = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(created.id).json()
        )
        by_email = RegisterUserResponse.model_validate(
            super_admin.api.user_api.get_user(creation_user_data["email"]).json()
        )

        assert by_id == by_email, "Содержание ответов должно быть идентичным"
        assert by_id.id, "ID должен быть не пустым"
        assert by_id.email == creation_user_data["email"]
        assert by_id.fullName == creation_user_data["fullName"]
        assert by_id.roles == ["USER"]
        assert by_id.verified is True