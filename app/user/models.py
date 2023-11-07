from app.database import Base
from sqlalchemy import JSON, String, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40))
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    training_batch_size: Mapped[int] = mapped_column(Integer, default=20)
    birth_date: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)

