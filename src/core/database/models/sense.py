from datetime import datetime

from src.core.database import Base
from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from . import User, Literature, Answer

from src.core.types import sense_status_type


class Sense(Base):
    f_sense_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), server_default=func.now()
    )
    status: Mapped[sense_status_type] = mapped_column(default="in_queue")

    literature_id: Mapped[int] = mapped_column(ForeignKey("literature.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    literature: Mapped["Literature"] = relationship(back_populates="senses")
    user: Mapped["User"] = relationship(back_populates="senses")
    word_images: Mapped[list["WordImage"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    sense_images: Mapped[list["SenseImage"]] = relationship(
        back_populates="sense", cascade="all, delete-orphan"
    )
    answers: Mapped[list["Answer"]] = relationship(back_populates="sense")


class WordImage(Base):
    f_img_id: Mapped[int]

    sense_id: Mapped["Sense"] = mapped_column(ForeignKey("sense.id"))
    sense: Mapped["Sense"] = relationship(back_populates="word_images")


class SenseImage(Base):
    f_img_id: Mapped[int]

    sense_id: Mapped["Sense"] = mapped_column(ForeignKey("sense.id"))
    sense: Mapped["Sense"] = relationship(back_populates="sense_images")
