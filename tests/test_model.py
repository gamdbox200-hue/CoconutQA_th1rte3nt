from models.registration_user_model import RegistrationUser
def test_model():
    user = RegistrationUser(
    email="test@test.com",
    fullName="Test User",
    password="Pass1234!",
    passwordRepeat="Pass1234!",
    roles=["USER"]
    )

    print(user)
    print(user.model_dump())
    print(user.email)