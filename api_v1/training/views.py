from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession
from . import train_generator
from core.database import db_helper
from core.database.models import User
from api_v1.user import get_current_user
from . import crud
from .scemas import SAnswer

router = APIRouter(prefix="/training", tags=["training"])


@router.get(
    "/",
    summary="Get training",
)
async def get_training(
    number: Annotated[int, Query(ge=1)],
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await train_generator.generate(session, user, number)


@router.post(
    "/",
    summary="Add answer",
)
async def get_training(
    answer: SAnswer,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_answer(session, user, answer)
