from pydantic import BaseModel, Field


class SAddSenseRequest(BaseModel):
    f_sense_id: int
    literature_id: int | None = None
    f_word_image_ids: list[int]
    f_sense_image_ids: list[int]


class SRequestUpdatePersonalSense(BaseModel):
    definition: str | None = None
    part_of_speech: str | None = None
    examples: list[str] | None = None
    images_base64str: list[str] | None = None
