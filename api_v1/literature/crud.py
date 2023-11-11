from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database.models import Literature


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
