import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import Field, EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    last_verification_request: datetime | None = None


class UserCreate(schemas.CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
