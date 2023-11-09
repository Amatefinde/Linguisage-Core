from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str

    birth_date: datetime | None = None


class UserCreateSchema(UserBaseSchema):
    password: str
    pass


class UserResponseSchema(UserBaseSchema):
    id: int
    registration_date: datetime


class UserSchema(UserBaseSchema):
    id: int
    hash_password: str
    registration_date: datetime
    birth_date: Optional[datetime]
