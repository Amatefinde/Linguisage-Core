from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.models import Literature
from datetime import datetime


async def get_literature_by_id(
    session: AsyncSession,
    literature_id: int,
) -> Literature | None:
    literature_db = await session.get(Literature, literature_id)
    return literature_db


async def get_all_user_literature(
    session: AsyncSession,
    user_id: int,
) -> list[Literature]:
    stmt = select(Literature).where(Literature.user_id == user_id)
    literature_db = await session.scalars(stmt)
    literature_db = list(literature_db)
    return literature_db


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
