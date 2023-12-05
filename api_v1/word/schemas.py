from pydantic import BaseModel, Field, ConfigDict, field_validator
from core.providers.Dictionary import SenseDTO
from typing import Literal


class SSenseNeuralResponseScheme(BaseModel):
    """Scheme for validate answer by NeuralMS"""

    idx: int
    sense: str
    spentTime: float


class SPairUserAndSense(BaseModel):
    f_sense_id: int = Field(ge=1)
    f_images_id: list[int] = Field(default=[])
    literature_id: int | None = Field(ge=1, default=None)
    status: Literal["complete", "in_process", "in_queue"] = "in_queue"


class SPairSenseAndImages(BaseModel):
    f_sense_id: int
    f_images_id: list[int]


class SResponseSenses(BaseModel):
    id: int
    sense: SenseDTO


#################################
class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ImageDTO(BaseDTO):
    f_img_id: int

    model_config = ConfigDict(from_attributes=True)


class SenseWithImagesDTO(BaseDTO):
    f_sense_id: int
    images: list[ImageDTO]

    model_config = ConfigDict(from_attributes=True)
