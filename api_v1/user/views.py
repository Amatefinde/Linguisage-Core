from fastapi import APIRouter, HTTPException, status, Depends, Response, Request, Header
from fastapi.security import OAuth2PasswordRequestForm

from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import (
    UserSchema,
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
    LoginUserSchema,
    SessionSchema,
)
from core.database import db_helper
from core.database.models import User
from typing import List, Annotated
from .dependencies import user_by_id, user_by_email, get_current_user
from api_v1.auth_tools.auth import verify_password, create_token

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
    request: Request,
    response: Response,
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_agent: Annotated[str | None, Header()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_data_from_db = await crud.get_user_by_email(
        email=user_data.username, session=session
    )
    if not user_data_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_data.username} bot found",
        )
    is_valid_password = verify_password(
        user_data.password, user_data_from_db.hash_password
    )
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password"
        )

    refresh_token = create_token(user_data_from_db.id, "Refresh")
    access_token = create_token(user_data_from_db.id, "Access")

    user_session = SessionSchema(
        user_id=user_data_from_db.id,
        ip=request.client.host,
        browser_header=user_agent,
        token=refresh_token,
    )

    await crud.add_user_session(session=session, user_session=user_session)

    response.set_cookie(
        key="linguisage_refresh_token",
        value=refresh_token,
        httponly=True,
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me", response_model=UserResponseSchema | None)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


# @router.get("/log_out/", status_code=status.HTTP_204_NO_CONTENT)
# async def login_user(
#     request: Request,
#     response: Response,
#     user_agent: Annotated[str | None, Header()] = None,
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     refresh_token = request.cookies.get("linguisage_refresh_token")
#
#     user_session = SessionSchema(
#         user_id=user_data_from_db.id,
#         ip=request.client.host,
#         browser_header=user_agent,
#         token=refresh_token,
#     )
#
#     response.delete_cookie("linguisage_refresh_token")
#
#     await crud.delete_user_session(session=session, user_session=user_session)
