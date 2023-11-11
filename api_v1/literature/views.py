from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.database import db_helper


router = APIRouter(prefix="/literature", tags=["Literature"])


@router.get("/", summary="Get literature by literature_id")
async def get_literature(
    literature_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_literature_by_id(session=session, literature_id=literature_id)


@router.get("/all", summary="Get all user literature by user_id")
async def get_literature(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_user_literature(session=session, user_id=user_id)
