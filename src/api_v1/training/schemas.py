from pydantic import BaseModel


class AnswerRequest(BaseModel):
    sense_id: int
    is_correct: bool
