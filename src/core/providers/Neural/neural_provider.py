from src.core.config import settings
from .schemas import WSDResponse
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError


class GetMeaningError(Exception):
    pass


async def get_meaning(word: str, context: str, senses: list[str]) -> WSDResponse:
    if not senses:
        raise ValueError("meanings can be list with elements")
    request = {"word": word, "context": context, "meanings": senses}
    async with aiohttp.ClientSession() as aiohttp_session:
        try:
            row_response = await aiohttp_session.post(
                settings.neural_module_url + "/get_meaning", json=request
            )
        except ClientConnectorError:
            raise GetMeaningError()
        if row_response.status != 200:
            raise GetMeaningError(f"Nural model return {row_response.status} code")
        response = await row_response.json()
        meaning_response = WSDResponse.model_validate(response)
        return meaning_response
