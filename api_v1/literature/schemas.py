from pydantic import BaseModel
from datetime import datetime


class LiteratureResponseScheme(BaseModel):
    id: int
    title: str
    add_datetime: datetime
    last_open_datetime: datetime | None = None
    user_id: int
