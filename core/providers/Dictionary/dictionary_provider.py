import asyncio

from aiohttp import ClientSession

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


async def _get_sense_with_image(session: ClientSession, sense: "SenseWithImagesDTO"):
    url = settings.DICTIONARY_MC_URL + f"/api/v1/words/sense/{sense.f_sense_id}"
    params = {"images_id": [img.f_img_id for img in sense.images]}

    async with session.get(url, params=params) as response:
        if response.status == 200:
            return SSenseP.model_validate(await response.json())


async def get_sense_with_images(sense: "SenseWithImagesDTO") -> SSenseP:
    async with aiohttp.ClientSession() as session:
        return await _get_sense_with_image(session, sense)


async def get_senses_with_images(senses: list["SenseWithImagesDTO"]) -> list[SSenseP]:
    async with aiohttp.ClientSession() as session:
        tasks = [_get_sense_with_image(session, sense) for sense in senses]
        return await asyncio.gather(*tasks)
