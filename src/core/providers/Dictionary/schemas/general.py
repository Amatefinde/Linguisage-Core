from pydantic import BaseModel, HttpUrl, Field
from src.core import types


class WordImage(BaseModel):
    is_public: bool
    f_image_id: int
    img: HttpUrl


class Example(BaseModel):
    id: int
    example: str
    html_example: str


class Sense(BaseModel):
    is_public: bool
    definition: str
    part_of_speech: str | None = None
    f_sense_id: int
    lvl: types.sense_lvl_type | None = None
    short_cut: str | None = None
    examples: list[Example]
    in_user_dictionary: bool = False


class DictionaryWordInfo(BaseModel):
    word: str
    f_word_id: int
    sound_uk: HttpUrl | None = None
    sound_us: HttpUrl | None = None
    word_images: list[WordImage]
    senses: list[Sense]


##################


class SRequestAddPersonalizeSense(BaseModel):
    word: str
    literature_id: int | None = None
    definition: str
    part_of_speech: str | None = None
    images_base64str: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)


class SenseImage(BaseModel):
    f_img_id: int = Field(validation_alias="id")


class PersonalizeSenseEntity(BaseModel):
    f_sense_id: int = Field(validation_alias="id")
    sense_images: list[SenseImage]


###################
