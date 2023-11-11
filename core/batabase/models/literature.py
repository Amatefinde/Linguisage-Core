from core.batabase.base import Base

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Literature(Base):
    title: Mapped[str]
    content: Mapped[int] = mapped_column(unique=True)
    add_datetime: Mapped[datetime] = mapped_column(TIMESTAMP)
    last_open_datetime: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    user: Mapped["User"] = mapped_column(ForeignKey("user_account.id"))
