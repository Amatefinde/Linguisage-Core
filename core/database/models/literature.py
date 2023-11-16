from core.database.base import Base

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Literature(Base):
    title: Mapped[str]
    content: Mapped[int] = mapped_column(unique=True)
    add_datetime: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow()
    )
    last_open_datetime: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="literatures")
