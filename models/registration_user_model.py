from typing import Optional
from pydantic import BaseModel, field_validator
from enmus.roles import Roles

class RegistrationUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email должен содержать @")
        return value

    @field_validator("password", "passwordRepeat")
    @classmethod
    def validate_password_length(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        return value

class RegisterUserResponse(BaseModel):
    model_config = {"extra": "forbid"}

    id: str
    email: str
    fullName: str
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str

class LoginResponse(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    user: dict


class ErrorResponse(BaseModel):
    message: str | list[str]
    error: str
    statusCode: int