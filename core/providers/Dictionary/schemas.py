from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, Field


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ExamplesDTO(BaseDTO):
    example: str


class RowExamplesDTO(BaseDTO):
    row_example: str


class ImageDTO(BaseDTO):
    id: int
    img: str


class SenseDTO(BaseDTO):
    id: int
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    short_cut: str | None = None
    definition: str
    examples: list[ExamplesDTO] = None
    row_examples: list[RowExamplesDTO] = None
    images: list[ImageDTO] = None


class WordDTO(BaseDTO):
    id: int
    word: str
    current_sense_id: int | None = None
    senses: list[SenseDTO]


###################################


class SBaseP(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SExamplesP(SBaseP):
    example: str


class SRowExamplesP(SBaseP):
    row_example: str


class SImageP(SBaseP):
    id: int
    img: str


class SWordForSenseP(SBaseP):
    word: str


class SSenseP(SBaseP):
    f_sense_id: int | None = Field(default=None, alias="id")
    lvl: Literal["A1", "A2", "B1", "B2", "C1", "C2"] | None = None
    short_cut: str | None = None
    definition: str
    status: Literal["complete", "in_process", "in_queue"] | None = None
    score: float | None = None
    examples: list[SExamplesP] = None
    row_examples: list[SRowExamplesP] = None
    images: list[SImageP] = None

    word: SWordForSenseP | None = None
