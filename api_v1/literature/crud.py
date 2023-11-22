import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from core.database.models import Literature
from datetime import datetime
import aiohttp
from .schemas import LiteratureResponseScheme


async def get_literature_by_id(
    session: AsyncSession,
    literature_id: int,
) -> Literature | None:
    literature_db = await session.get(Literature, literature_id)
    return literature_db


async def get_literature_cover(session, literature_id):
    params = {
        "literature_id": literature_id,
        "start_page": 1,
        "end_page": 1,
    }
    url = settings.content_manager_url + "/literature/get_pages"
    async with session.get(url, params=params) as resp:
        try:
            return await resp.json()
        except Exception:
            return None


async def get_all_user_literature(
    session: AsyncSession,
    user_id: int,
) -> list[LiteratureResponseScheme]:
    stmt = select(Literature).where(Literature.user_id == user_id)

    literature_db = await session.scalars(stmt)
    literatures = [LiteratureResponseScheme(**x.__dict__) for x in literature_db]
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_literature_cover(session, instance.content) for instance in literatures
        ]

        books = await asyncio.gather(*tasks)
        covers = [
            (x[0]["img"] if len(x) else None) if type(x) is list else None
            for x in books
        ]

    for idx, literature in enumerate(literatures):
        literature.cover = covers[idx]

    return literatures


async def add_literature_by_user_id(
    session: AsyncSession,
    title: str,
    user_id: int,
    content_id: int,
):
    db_literature = Literature(
        title=title, content=content_id, add_datetime=datetime.utcnow(), user_id=user_id
    )

    session.add(db_literature)
    await session.commit()
    await session.refresh(db_literature)
    return db_literature


async def delete_literature(
    session: AsyncSession,
    db_literature: Literature,
):
    await session.delete(db_literature)
    await session.commit()


async def get_last_opened(session: AsyncSession, user_id: int):
    stmt = (
        select(Literature)
        .where(Literature.user_id == user_id)
        .order_by(Literature.last_open_datetime.desc(), Literature.add_datetime.desc())
    )
    result = await session.scalar(stmt)
    return result
