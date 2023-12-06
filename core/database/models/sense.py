from datetime import datetime

from core.database import Base
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from . import User, Literature, Answer

status = Enum("complete", "in_process", "in_queue", name="word_status")


class Sense(Base):
    f_sense_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), server_default=func.now()
    )
    status: Mapped[str] = mapped_column(status, default="in_queue")

    literature_id: Mapped[int] = mapped_column(
        ForeignKey("literature.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    literature: Mapped["Literature"] = relationship(back_populates="senses")
    user: Mapped["User"] = relationship(back_populates="senses")
    images: Mapped[list["Image"]] = relationship(
        back_populates="senses", cascade="all, delete-orphan"
    )
    answers: Mapped[list["Answer"]] = relationship(back_populates="sense")


class Image(Base):
    f_img_id: Mapped[int]

    sense_id: Mapped["Sense"] = mapped_column(ForeignKey("sense.id"))
    senses: Mapped["Sense"] = relationship(back_populates="images")
