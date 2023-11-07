from fastapi import APIRouter, HTTPException

from . import crud
from .schemas import UserSchema, UserCreateSchema

router = APIRouter(prefix="users", tags=["Users"])


@router.get("/", response_model=list(UserSchema))
async def get_users(session):
    return await crud.get_users()


@router.post("/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, session):
    pass


@router.get("/{user_id}/", response_model=UserSchema)
async def get_user(user_id: int, session):
    user = await crud.get_user(session=session, user_id=user_id)
    if user:
        return user

    raise HTTPException(
        status_code=404,
        detail=f"User with id {user_id} is not found",
    )
