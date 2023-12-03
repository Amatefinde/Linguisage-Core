from pydantic import BaseModel, ConfigDict
from core.providers.Dictionary import SenseDTO


class SSenseNeuralResponseScheme(BaseModel):
    """Scheme for validate answer by NeuralMS"""

    idx: int
    sense: str
    spentTime: float


class SPairUserAndSense(BaseModel):
    f_sense_id: int
    literature_id: int | None = None
    status: str = "in_queue"


class SPairSenseAndImages(BaseModel):
    f_sense_id: int
    f_images_id: list[int]


class SResponseSenses(BaseModel):
    id: int
    sense: SenseDTO
