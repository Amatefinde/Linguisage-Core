from core.config import settings
from .schemas import WordDTO
import aiohttp


async def get_word_by_query(query: str, download_if_not_found=True) -> WordDTO | None:
    url = settings.DICTIONARY_MC_URL + "/api/v1/words/alias"
    params = {
        "alias": query,
        "download_if_not_found": str(download_if_not_found).lower(),
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                word = WordDTO.model_validate(await response.json())
                return word
