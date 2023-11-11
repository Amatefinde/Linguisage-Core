from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.database.models import User
from . import crud
from core.database import db_helper
from api_v1.user import get_current_user

router = APIRouter(prefix="/literature", tags=["Literature"])


@router.get("/all", summary="Get all user literature by user_id")
async def get_literature(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_user_literature(session=session, user_id=current_user.id)
