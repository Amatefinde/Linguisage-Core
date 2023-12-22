import requests
from os import path

from aiohttp import ClientTimeout

from core.config import settings
import aiohttp


async def add_literature(file, use_ocr: bool = False) -> int | None:
    url = settings.content_manager_url + "/literature/add"
    data = aiohttp.FormData()
    data.add_field("file", file, filename="image.jpg")
    timeout = ClientTimeout(total=60 * 60 * 3)  # Set timeout to 3 hours seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            url, data=data, params={"use_ocr": str(use_ocr).lower()}
        ) as response:
            if response.status != 200:
                return
            return int(await response.json())


async def get_literature_pages(
    content_id: int, start_page: int = 1, end_page: int = 0
) -> dict:
    url = settings.content_manager_url + "/literature/get_pages"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            params={
                "literature_id": content_id,
                "start_page": start_page,
                "end_page": end_page,
            },
        ) as response:
            if response.status != 200:
                return
            return await response.json()


async def delete_literature(f_file_id) -> int:
    url = settings.content_manager_url + "/literature/delete"
    timeout = ClientTimeout(total=60 * 60 * 3)  # Set timeout to 3 hours seconds
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.delete(
            url, params={"literature_id": f_file_id}
        ) as response:
            if response.status != 200:
                return
            return int(await response.json())