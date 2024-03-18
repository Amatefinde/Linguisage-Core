from typing import Annotated
from fastapi import Path, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import Sense, User


async def sense_dependency(
    sense_id: Annotated[int, Path()],
    current_user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_sense = await db_session.get(Sense, sense_id)
    if db_sense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if db_sense.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_sense
