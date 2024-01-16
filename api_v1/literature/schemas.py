from pydantic import BaseModel, ConfigDict
from datetime import datetime


class LiteratureResponseScheme(BaseModel):
    id: int
    title: str
    add_datetime: datetime
    last_open_datetime: datetime | None = None
    user_id: int
    cover: str | None = None
    f_literature_id: int

    model_config = ConfigDict(from_attributes=True)


class LiteratureStatsScheme(BaseModel):
    literature_id: int
    complete: int = 0
    in_queue: int = 0
    in_process: int = 0
    total: int = 0
