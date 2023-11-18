from core.database import Base
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from . import User, Literature

status = Enum("complete", "in_process", "in_queue", name="word_status")


class UserWordMeaning(Base):
    content: Mapped[int]
    status: Mapped[str] = mapped_column(status)
    literature_id: Mapped[int] = mapped_column(
        ForeignKey("literature.id"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    literature: Mapped["Literature"] = relationship(back_populates="words")
    user: Mapped["User"] = relationship(back_populates="words")
    images: Mapped[list["UserWordImage"]] = relationship(
        back_populates="user_word_meaning", cascade="all, delete-orphan"
    )


class UserWordImage(Base):
    content: Mapped[int]
    user_word_meaning_id: Mapped["UserWordMeaning"] = mapped_column(
        ForeignKey("userwordmeaning.id")
    )

    user_word_meaning: Mapped["UserWordMeaning"] = relationship(back_populates="images")
