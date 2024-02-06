from sqlalchemy import ForeignKey
from src.core.database import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import Sense, User


class Answer(Base):
    is_correct: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), server_default=func.now()
    )
    sense_id: Mapped[int] = mapped_column(ForeignKey("sense.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    sense: Mapped["Sense"] = relationship(back_populates="answers")
    user: Mapped["User"] = relationship(back_populates="answers")
