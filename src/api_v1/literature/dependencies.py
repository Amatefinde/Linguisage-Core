from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from src.core.database import db_helper
from src.core.database.models import User, Literature
from src.api_v1.user.user_manager import current_active_user_dependency


async def literature_dependency(
    literature_id: Annotated[int, Path()],
    db_session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
) -> Literature:
    db_literature = await crud.get_literature(db_session, literature_id)
    if db_literature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Literature with id {literature_id} not found",
        )
    if db_literature.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_literature
