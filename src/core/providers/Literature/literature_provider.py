import httpx
from typing import Sequence, TYPE_CHECKING
from urllib.parse import urljoin
from fastapi import UploadFile, HTTPException
from loguru import logger

from src.core import settings
from .scheme import LiteratureEpubEntity, ManyLiteratureEpubEntity, SPatchRequest


async def add_book(file: UploadFile, user_chosen_filename: str) -> LiteratureEpubEntity:
    async with httpx.AsyncClient() as httpx_client:
        url = urljoin(settings.ms.LITERATURE_MS_URL, "api/v1/books")
        files = {"file": (file.filename, file.file)}
        response = await httpx_client.post(
            url, files=files, data={"filename": user_chosen_filename}
        )
        if response.status_code != 201:
            logger.error(response.json())
        book_entity = LiteratureEpubEntity.model_validate(response.json(), from_attributes=True)
        return book_entity


async def get_many_book(f_literature_ids: Sequence[int]) -> ManyLiteratureEpubEntity:
    async with httpx.AsyncClient() as httpx_client:
        url = urljoin(settings.ms.LITERATURE_MS_URL, "api/v1/books")
        response = await httpx_client.get(url, params={"id": f_literature_ids})
        if response.status_code != 200:
            logger.error(response.json())
        books = ManyLiteratureEpubEntity.model_validate(response.json(), from_attributes=True)
        return books


async def delete_book(f_literature_id: int) -> None:
    async with httpx.AsyncClient() as httpx_client:
        url = urljoin(settings.ms.LITERATURE_MS_URL, f"api/v1/books/{f_literature_id}")
        response = await httpx_client.delete(url)
        if response.status_code != 204:
            logger.error(response.text)
            raise HTTPException(status_code=500)


async def patch_book(f_literature_id: int, patch: SPatchRequest) -> LiteratureEpubEntity:
    async with httpx.AsyncClient() as httpx_client:
        url = urljoin(settings.ms.LITERATURE_MS_URL, f"api/v1/books/{f_literature_id}")
        response = await httpx_client.patch(url, json=patch.model_dump())
        if response.status_code != 200:
            logger.error(response.text)
            raise HTTPException(status_code=500, detail="Unsuccessful request to Literature MS")
        return LiteratureEpubEntity.model_validate(response.json(), from_attributes=True)
