from datetime import datetime

from pydantic import BaseModel, HttpUrl


class LiteratureEpubEntity(BaseModel):
    cover: HttpUrl | None = None
    created_at: datetime
    id: int
    is_processed: bool
    last_opened_at: datetime | None = None
    last_read_position: int | None = None
    original_file: HttpUrl
    title: str


class ManyLiteratureEpubEntity(BaseModel):
    books: list[LiteratureEpubEntity]


class SPatchRequest(BaseModel):
    title: str
