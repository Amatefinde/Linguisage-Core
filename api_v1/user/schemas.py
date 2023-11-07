from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    name: str
    password: str
    birth_date: Optional[str]


class UserCreateSchema(UserBaseSchema):
    pass


class UserSchema(BaseModel):
    id: int
    registration_date: datetime
