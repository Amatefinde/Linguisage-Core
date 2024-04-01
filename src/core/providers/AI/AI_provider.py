from fastapi import HTTPException
from httpx import AsyncClient
from urllib.parse import urljoin

from loguru import logger

from src.core import settings
from .schemas import RequestSenseReview, SenseReview


async def review(request_sense_review: RequestSenseReview) -> SenseReview:
    async with AsyncClient() as httpx_client:
        url = urljoin(settings.ms.AI_MS_URL, "/review-sentence")

        response = await httpx_client.post(
            url, json=request_sense_review.model_dump(), timeout=10.0
        )

        if response.status_code == 200:
            return SenseReview.model_validate(response.json())
        raise HTTPException(
            detail="At this moment AI review not available", status_code=response.status_code
        )
