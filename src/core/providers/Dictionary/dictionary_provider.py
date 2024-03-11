from pprint import pprint

from fastapi import HTTPException
from httpx import AsyncClient
from urllib.parse import urljoin

from loguru import logger

from src.core import settings
from .schemas.entity import SenseEntities
from .schemas.general import (
    DictionaryWordInfo,
    SRequestAddPersonalizeSense,
    PersonalizeSenseEntity,
)
from .schemas.get_senses import SGetSense


async def search(query: str) -> DictionaryWordInfo:
    async with AsyncClient() as httpx_client:
        url = urljoin(settings.ms.DICTIONARY_MS_URL, "/api/v1/public/query")
        response = await httpx_client.get(url, params={"query": query})
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Sorry, we don't have info about {query!r}, "
                f"but if this word exists, we already try to search info about it. "
                f"You may try again after several tens of seconds",
            )
        elif response.status_code == 200:
            return DictionaryWordInfo.model_validate(response.json())
        raise HTTPException(detail=response.text, status_code=response.status_code)


async def add_personalize_sense(
    add_scheme: SRequestAddPersonalizeSense,
) -> PersonalizeSenseEntity:
    async with AsyncClient() as httpx_client:
        url = urljoin(settings.ms.DICTIONARY_MS_URL, "/api/v1/personalize")
        response = await httpx_client.post(url, json=add_scheme.model_dump())
        if response.status_code == 201:
            return PersonalizeSenseEntity.model_validate(response.json(), from_attributes=True)

        logger.error(f"status: {response.status_code}. {response.text}")
        raise HTTPException(detail=response.text, status_code=response.status_code)


async def get_senses(
    get_senses_scheme: list[SGetSense],
) -> SenseEntities:
    async with AsyncClient() as httpx_client:
        senses = {"senses": [x.model_dump() for x in get_senses_scheme]}
        url = urljoin(settings.ms.DICTIONARY_MS_URL, "/api/v1/general/get_senses")
        response = await httpx_client.post(url, json=senses)
        if response.status_code == 200:
            return SenseEntities.model_validate(response.json(), from_attributes=True)

        logger.error(f"status: {response.status_code}. {response.text}")
        raise HTTPException(detail=response.text, status_code=response.status_code)
