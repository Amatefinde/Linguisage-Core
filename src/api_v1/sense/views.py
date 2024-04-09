from fastapi import APIRouter, Depends, status, HTTPException, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from . import crud
from .dependencies import sense_dependency
from .scheme.request import SAddSenseRequest
from src.core.providers.Dictionary import dictionary_provider
from src.core.providers.Dictionary.schemas.general import DictionaryWordInfo
from src.core.providers.Dictionary.schemas.general import SRequestAddPersonalizeSense
from src.api_v1.user.user_manager import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import User, Sense
from src.core.types import sense_lvl_type
from src.core.providers.Dictionary.schemas.get_senses import SGetSense

router = APIRouter(prefix="/senses", tags=["Senses"])


@router.get("")
async def get_user_senses(
    new_first: bool = False,
    per_page: int | None = None,
    page: int | None = None,
    query: str | None = None,
    # lvl: Annotated[list[sense_lvl_type] | None, Query()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    query = query if query else None
    lvl = None
    if query or lvl:
        db_senses: list[SGetSense] = await crud.get_senses(session, user, new_first=new_first)
        dictionary_senses = await dictionary_provider.get_senses(db_senses, query=query, lvl=lvl)
    else:
        db_senses: list[SGetSense] = await crud.get_senses(
            session, user, page=page, limit=per_page, new_first=new_first
        )
        dictionary_senses = await dictionary_provider.get_senses(db_senses)
    return dictionary_senses


@router.get("/search", response_model=DictionaryWordInfo)
async def search(
    query: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    dictionary_word_info = await dictionary_provider.search(query)
    await crud.mark_senses_that_user_already_have(session, user, dictionary_word_info)
    return dictionary_word_info


@router.post("/public", status_code=status.HTTP_201_CREATED)
async def add_public_sense_to_user(
    add_scheme: SAddSenseRequest,
    user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    if await crud.check_is_user_have_sense_by_f_sense_id(db_session, user, add_scheme.f_sense_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already has sense")
    return await crud.add_public_sense_to_user(db_session, user, add_scheme)


@router.post("/personalize", status_code=status.HTTP_201_CREATED)
async def add_personalize_sense_to_user(
    add_scheme: SRequestAddPersonalizeSense,
    user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    personalize_sense_entity = await dictionary_provider.add_personalize_sense(add_scheme)
    return await crud.add_personalize_sense_to_user(
        db_session,
        user,
        personalize_sense_entity,
        literature_id=add_scheme.literature_id,
    )


@router.delete("/{sense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sense(
    db_sense: Sense = Depends(sense_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    await db_session.delete(db_sense)
    await db_session.commit()
