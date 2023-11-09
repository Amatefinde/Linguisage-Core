from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud
from .schemas import UserSchema, UserCreateSchema
from core.models import db_helper
from asyncpg.exceptions import UniqueViolationError

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_users(session=session)


# @router.post("/", response_model=UserSchema)
@router.post("/")
async def create_user(
    user: UserCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_user = crud.get_user_by_email(session=session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Probably user with this email is already exist",
        )

    return await crud.add_user(session=session, user=user)


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(
    user_id: int, session: AsyncSession = Depends(db_helper.session_dependency)
):
    user = await crud.get_user_by_id(user_id=user_id, session=session)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} is not found",
    )
