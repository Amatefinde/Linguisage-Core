import uuid
from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str
    last_verification_request: datetime


class UserUpdate(schemas.BaseUserUpdate):
    pass
