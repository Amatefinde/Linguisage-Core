from pydantic import BaseModel, Field


class WSDResponse(BaseModel):
    idx: int = Field(ge=0)
    meaning: str
    spent_time: float = Field(alias="spentTime")
