from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from . import crud
from core.database import db_helper
from core.database.models import User
from fastapi import Body, Path

from .schemas import LoginUserSchema


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user = await crud.get_user_by_id(user_id=user_id, session=session)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} is not found",
    )


async def user_by_email(
    user_data: LoginUserSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> User:
    user_email = user_data.email
    user = await crud.get_user_by_email(email=user_email, session=session)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with email "{user_email}" is not found',
    )
