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
from ...types import sense_lvl_type


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
    query: str | None = None,
    lvl: list[sense_lvl_type] | None = None,
) -> SenseEntities:
    f_sense_id_and_sense_id_map = {x.sense_id: x for x in get_senses_scheme}
    async with AsyncClient() as httpx_client:
        params = {"senses": [x.model_dump() for x in get_senses_scheme]}
        if query is not None:
            params.update({"clauses": {"search": query}})
        if lvl:
            params["lvl"] = lvl
        url = urljoin(settings.ms.DICTIONARY_MS_URL, "/api/v1/general/get_senses")
        response = await httpx_client.post(url, json=params)
        if response.status_code == 200:
            sense_entities = SenseEntities.model_validate(response.json(), from_attributes=True)
            for sense in sense_entities.senses:
                sense.status = f_sense_id_and_sense_id_map[sense.id].status
                # поле айди перезаписывать последним, потому что по нему перезаписываются остальные поля
                sense.id = f_sense_id_and_sense_id_map[sense.id].id
            return sense_entities

        logger.error(f"status: {response.status_code}. {response.text}")
        raise HTTPException(detail=response.text, status_code=response.status_code)
