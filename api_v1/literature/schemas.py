from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LiteratureResponseScheme(BaseModel):
    id: int
    title: str
    add_datetime: datetime
    last_open_datetime: datetime | None = None
    user_id: int
    cover: str | None = None
    content: int

    model_config = ConfigDict(from_attributes=True)
