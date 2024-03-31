from pydantic import BaseModel, ConfigDict


class RequestSenseReview(BaseModel):
    word: str
    sense: str
    sentence: str


class SenseReview(BaseModel):
    score: int
    feedback: str
    explanation: str

    model_config = ConfigDict(from_attributes=True)
