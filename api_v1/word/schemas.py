from pydantic import BaseModel, ConfigDict


class MeaningResponseScheme(BaseModel):
    idx: int
    meaning: str
    spentTime: float


class UserWordMeaningRequestScheme(BaseModel):
    content: int
    literature_id: int | None = None
    status: str = "in_queue"


class UserWordMeaningScheme(UserWordMeaningRequestScheme):
    user_id: int


class Image(BaseModel):
    content: int
    model_config = ConfigDict(from_attributes=True)


class LinkMeaningWithImagesScheme(BaseModel):
    id: int
    content: int
    images: list[Image]

    model_config = ConfigDict(from_attributes=True)


class UserWordMeaningResponseScheme(BaseModel):
    word: str
    meaning: str
    short_meaning: str
