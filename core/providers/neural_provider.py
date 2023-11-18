import requests
from core.config import settings
from api_v1.word.schemas import MeaningResponseScheme


def get_meaning(word: str, context: str, meanings: list[str]) -> MeaningResponseScheme:
    if not meanings:
        raise ValueError("meanings can be list with elements")
    request = {"word": word, "context": context, "meanings": meanings}
    response = requests.post(settings.neural_module_url + "/get_meaning", json=request)
    meaning_response = MeaningResponseScheme(**dict(response.json()))
    return meaning_response
