from typing import Optional, List
from src.core.types import sense_lvl_type, sense_status_type
from pydantic import HttpUrl, BaseModel, Field


class WordImage(BaseModel):
    img: HttpUrl
    is_public: bool
    id: int = Field(serialization_alias="f_image_id")


class SenseImage(BaseModel):
    img: HttpUrl
    is_public: bool
    id: int


class Example(BaseModel):
    html_example: str
    example: str
    id: int


class Sense(BaseModel):
    id: int = None
    status: sense_status_type | None = None
    f_sense_id: int | None = Field(default=None, validation_alias="id")
    short_cut: Optional[str] = None
    part_of_speech: str | None = None
    lvl: sense_lvl_type | None = None
    is_public: bool
    definition: str
    word_images: List[WordImage]
    sense_images: List[SenseImage]
    word: dict
    examples: List[Example]


class SenseEntities(BaseModel):
    senses: List[Sense]
