from core.config import settings
from .schemas import WordDTO, SSenseP

import aiohttp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from api_v1.word.schemas import SenseWithImagesDTO


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


async def get_senses_with_images(sense: "SenseWithImagesDTO") -> SSenseP:
    url = settings.DICTIONARY_MC_URL + f"/api/v1/words/sense/{sense.f_sense_id}"
    params = {"images_id": [img.f_img_id for img in sense.images]}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return SSenseP.model_validate(await response.json())
