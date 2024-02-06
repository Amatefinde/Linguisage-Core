import asyncio

from aiohttp import ClientSession

from src.core.config import settings
from .schemas import WordDTO, SSenseP

import aiohttp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


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


async def get_senses_with_images_alt(senses: list["SenseWithImagesDTO"]) -> list[SSenseP]:
    url = settings.DICTIONARY_MC_URL + f"/api/v1/words/get_senses_with_images_by_id"
    body_params = {"senses": []}
    senses_with_images_ready: list[SSenseP] = []
    if not senses:
        return senses_with_images_ready
    for sense in senses:
        images_ids = [image.f_img_id for image in sense.images]
        body_params["senses"].append({"sense_id": sense.f_sense_id, "images_ids": images_ids})
    async with aiohttp.ClientSession() as session:
        row_response = await session.post(url, json=body_params)
        json_response = await row_response.json()
    for sense in json_response:
        senses_with_images_ready.append(SSenseP.model_validate(sense))
    return senses_with_images_ready
