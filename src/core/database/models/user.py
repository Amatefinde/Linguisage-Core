from typing import TYPE_CHECKING

from sqlalchemy import String, TIMESTAMP, Integer, DATE, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.testing.pickleable import User
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from src.core.database import db_helper
from src.core.database.base import Base
from src.core import types

if TYPE_CHECKING:
    from . import Literature, Sense, Answer


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str]
    last_verification_request: Mapped[datetime | None] = mapped_column(
        default=None, server_default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, server_default=func.now()
    )
    account_status: Mapped[types.account_status] = mapped_column(
        default="default", server_default="default"
    )
    literatures: Mapped[list["Literature"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    senses: Mapped[list["Sense"]] = relationship(back_populates="user")
    answers: Mapped[list["Answer"]] = relationship(back_populates="user")


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass


async def db_user_dependency(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


# class User(Base):
#     email: Mapped[str] = mapped_column(unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(40))
#     hash_password: Mapped[str] = mapped_column(String, nullable=False)
#     registered_at: Mapped[datetime] = mapped_column(
#         TIMESTAMP, default=datetime.utcnow()
#     )
#     training_batch_size: Mapped[int] = mapped_column(Integer, default=20)
#     birth_date: Mapped[date] = mapped_column(DATE, nullable=True)
#
#     sessions: Mapped[list["Session"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#     literatures: Mapped[list["Literature"]] = relationship(
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )
#
#     senses: Mapped[list["Sense"]] = relationship(back_populates="user")
#     answers: Mapped[list["Answer"]] = relationship(back_populates="user")


async def db_access_token_dependency(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
