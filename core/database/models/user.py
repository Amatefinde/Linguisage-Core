from core.database.base import Base
from sqlalchemy import JSON, String, TIMESTAMP, Integer, DATE, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .literature import Literature


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40))
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow()
    )
    training_batch_size: Mapped[int] = mapped_column(Integer, default=20)
    birth_date: Mapped[date] = mapped_column(DATE, nullable=True)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    literatures: Mapped[list["Literature"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Session(Base):
    token: Mapped[str]
    ip: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="sessions")