from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class SAnswer(BaseModel):
    f_sense_id: int
    is_correct: bool


class Image(BaseModel):
    f_img_id: int

    model_config = ConfigDict(from_attributes=True)


class AnswerDTO(BaseModel):
    is_correct: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SenseDTO(BaseModel):
    f_sense_id: int
    status: Literal["complete", "in_process", "in_queue"]
    answers: list[AnswerDTO] = []
    images: list[Image] = []

    model_config = ConfigDict(from_attributes=True)


class SExersice(BaseModel):
    word: str
    definition: str
    images: list[str] = []
    examples: list[str]
