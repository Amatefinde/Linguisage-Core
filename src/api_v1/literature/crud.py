from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import Literature, User
from src.core.providers.Literature.scheme import LiteratureEpubEntity, SPatchRequest


async def add_user_literature(
    session: AsyncSession,
    user: User,
    book_entity: LiteratureEpubEntity,
) -> Literature:
    db_literature = Literature(
        title=book_entity.title,
        f_literature_id=book_entity.id,
        user_id=user.id,
    )
    session.add(db_literature)
    await session.commit()

    return db_literature


async def get_all_user_literature(session: AsyncSession, user: User) -> Iterable[Literature]:
    stmt = select(Literature).where(Literature.user_id == user.id)
    return (await session.execute(stmt)).scalars()


async def get_literature(session: AsyncSession, literature_id: int) -> Literature | None:
    return await session.get(Literature, literature_id)


async def delete_literature(session: AsyncSession, db_literature: Literature):
    await session.delete(db_literature)
    await session.commit()


async def patch_literature(
    session: AsyncSession,
    db_literature: Literature,
    patch: SPatchRequest,
):
    db_literature.title = patch.title
    await session.commit()


async def get_last_user_literature(session: AsyncSession, user: User) -> Literature | None:
    stmt = (
        select(Literature)
        .where(Literature.user == user)
        .order_by(Literature.last_open_datetime, Literature.add_datetime)
        .limit(1)
    )
    return await session.scalar(stmt)
