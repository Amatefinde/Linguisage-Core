from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from . import crud
from core.database import db_helper
from core.database.models import User
from fastapi import Body, Path, Header, Request
from core.config import settings
from .schemas import LoginUserSchema
from api_v1.auth_tools.auth import decode_token


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/users/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_id = decode_token(token, token_type="Access")
    user_db = await crud.get_user_by_id(user_id=user_id, session=session)
    if user_db:
        return user_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
