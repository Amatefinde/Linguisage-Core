from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str
    birth_date: date | None = None


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponseSchema(UserBaseSchema):
    id: int
    registration_date: datetime


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr | None = None
    name: str | None = None
    birth_date: date | None = None
    password: str | None = None


class UserSchema(UserBaseSchema):
    id: int
    hash_password: str
    registration_date: datetime


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class SessionSchema(BaseModel):
    user_id: int
    token: str
    ip: str
    browser_header: str
