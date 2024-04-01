from typing import Optional

from pydantic import BaseModel, ConfigDict


class RequestSenseReview(BaseModel):
    word: str
    sense: str
    sentence: str


class SenseReview(BaseModel):
    score: int
    feedback: Optional[str] = None
    explanation: Optional[str] = None
    corrected_sentence: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
