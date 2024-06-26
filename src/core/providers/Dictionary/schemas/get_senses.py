from datetime import datetime

from pydantic import BaseModel, field_serializer, Field
from src.core.types import sense_status_type


class SenseImage(BaseModel):
    f_img_id: int


class WordImage(BaseModel):
    f_img_id: int


class SGetSense(BaseModel):
    id: int
    status: sense_status_type
    sense_id: int = Field(validation_alias="f_sense_id")
    sense_image_ids: list[SenseImage] = Field(validation_alias="sense_images")
    word_image_ids: list[WordImage] = Field(validation_alias="word_images")
    created_at: datetime | None = None

    @field_serializer("sense_image_ids")
    def serialize_sense_images(self, sense_images: list[SenseImage]):
        return [x.f_img_id for x in sense_images]

    @field_serializer("word_image_ids")
    def serialize_word_images(self, word_images: list[WordImage]):
        return [x.f_img_id for x in word_images]
