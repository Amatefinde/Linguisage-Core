from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import User


async def set_last_verification_date_by_now(session: AsyncSession, user: User) -> None:
    user.last_verification_request = datetime.now()
    await session.commit()
    await session.refresh(user)
