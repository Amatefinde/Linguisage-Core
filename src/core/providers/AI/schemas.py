from pydantic import BaseModel, ConfigDict
from typing_extensions import Optional


class RequestSenseReview(BaseModel):
    word: str
    sense: str
    sentence: str


class ReviewResponse(BaseModel):
    score: int
    feedback: Optional[str] = None
    explanation: Optional[str] = None
    corrected_sentence: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
