from fastapi import Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from api_v1.user import get_current_user
from core.database.models import User
from . import crud
from core.database import db_helper


async def current_user_literature_by_id(
    literature_id: Annotated[int, Query],
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    literature_db = await crud.get_literature_by_id(
        session=session, literature_id=literature_id
    )
    if not literature_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if literature_db.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return literature_db
