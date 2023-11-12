import requests
from os import path
from core.config import settings


def add_literature(file, use_ocr: bool = False) -> int | None:
    files = {"file": ("image.jpg", file)}
    url = settings.content_manager_url + "/literature/add"
    response = requests.post(url, files=files, params={"use_ocr": str(use_ocr).lower()})
    if response.status_code != 200:
        return
    return int(response.json())


def get_literature_pages(
    content_id: int, start_page: int = 1, end_page: int = 0
) -> dict:
    url = settings.content_manager_url + "/literature/get_pages"
    response = requests.get(
        url,
        params={
            "literature_id": content_id,
            "start_page": start_page,
            "end_page": end_page,
        },
    )
    if response.status_code != 200:
        return
    return response.json()
