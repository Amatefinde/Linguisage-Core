from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    declared_attr,
)

from src.core.config import settings

engine = create_async_engine(settings.db.url)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self):
        return self.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
