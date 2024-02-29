import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import Field, EmailStr

from src.core import types


class UserGeneralFieldMixin(schemas.CreateUpdateDictModel):
    username: str


class UserRead(schemas.BaseUser[uuid.UUID], UserGeneralFieldMixin):
    last_verification_request: datetime | None = None
    account_status: types.account_status


class UserCreate(UserGeneralFieldMixin):
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate, UserGeneralFieldMixin):
    pass
