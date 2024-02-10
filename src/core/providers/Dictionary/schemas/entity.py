from typing import Optional, List
from src.core.types import sense_lvl
from pydantic import HttpUrl, BaseModel


class WordImage(BaseModel):
    img: HttpUrl
    is_public: bool
    id: int


class SenseImage(BaseModel):
    img: HttpUrl
    is_public: bool
    id: int


class Example(BaseModel):
    html_example: str
    example: str
    id: int


class Sense(BaseModel):
    id: int
    short_cut: Optional[str] = None
    part_of_speech: str | None = None
    lvl: sense_lvl | None = None
    is_public: bool
    definition: str
    word_images: List[WordImage]
    sense_images: List[SenseImage]
    word: dict
    examples: List[Example]


class SenseEntities(BaseModel):
    senses: List[Sense]
