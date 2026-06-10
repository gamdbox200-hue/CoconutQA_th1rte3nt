import pytest
import allure
from pytest_check import check
from models.registration_user_model import RegistrationUser


@allure.feature("Model Validation")
@allure.story("Pydantic Model")
@allure.title("Валидация Pydantic-модели RegistrationUser")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_model():
    with allure.step("Создать экземпляр RegistrationUser"):
        user = RegistrationUser(
            email="test@test.com",
            fullName="Test User",
            password="Pass1234!",
            passwordRepeat="Pass1234!",
            roles=["USER"]
        )

    with allure.step("Проверить поля модели"):
        check.equal(user.email, "test@test.com")
        check.equal(user.fullName, "Test User")
        check.equal(user.password, "Pass1234!")
        check.equal(user.passwordRepeat, "Pass1234!")
        check.equal(user.roles, ["USER"])

    with allure.step("Проверить model_dump()"):
        dumped = user.model_dump()
        check.is_instance(dumped, dict)
        check.is_in("email", dumped)
        check.is_in("fullName", dumped)