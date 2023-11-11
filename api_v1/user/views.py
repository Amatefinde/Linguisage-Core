from fastapi import APIRouter, HTTPException, status, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import (
    UserSchema,
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
    LoginUserSchema,
)
from core.database import db_helper
from core.database.models import User
from typing import List
from .dependencies import user_by_id, user_by_email
from api_v1.auth_tools.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema])
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_users(session=session)


@router.post(
    path="/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_user = await crud.get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Probably user with this email is already exist",
        )

    return await crud.add_user(session=session, user=user)


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(user: User = Depends(user_by_id)):
    return user


@router.patch("/{user_id}/", response_model=UserSchema)
async def update_user(
    new_user: UserUpdateSchema,
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if (user.email != new_user.email) and (
        await crud.get_user_by_email(session=session, email=new_user.email)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with email "{new_user.email}" already exists',
        )

    return await crud.update_user_partition(
        session=session,
        user_id=user.id,
        new_user=new_user,
    )


@router.delete("/{user_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_user(session=session, user=user)


@router.post("/login/")
async def login_user(
    response: Response,
    user_data: LoginUserSchema,
    user_data_from_db: User = Depends(user_by_email),
):
    is_valid_password = verify_password(
        user_data.password, user_data_from_db.hash_password
    )
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password"
        )
    response.set_cookie(
        key="linguisage_refresh_token",
        value=create_refresh_token(user_data_from_db.id),
        httponly=True,
    )
    return create_access_token(user_data_from_db.id)


@router.get("/get_browser_info")
def get_browser_info(request: Request, field: int = 2):
    return request.client.host
