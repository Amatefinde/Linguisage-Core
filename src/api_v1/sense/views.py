from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .scheme.request import SAddSenseRequest
from src.core.providers.Dictionary import dictionary_provider
from src.core.providers.Dictionary.schemas.general import (
    DictionaryWordInfo,
    SRequestAddPersonalizeSense,
)
from src.api_v1.user.user_manager import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import User
from . import crud
from ...core.providers.Dictionary.schemas.get_senses import SGetSense

router = APIRouter(prefix="/senses", tags=["Senses"])


@router.get("")
async def get_user_senses(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    db_senses: list[SGetSense] = await crud.get_senses(session, user)
    f_sense_id_and_sense_id_map = {x.sense_id: x.id for x in db_senses}
    sense_entities = await dictionary_provider.get_senses(db_senses)
    for sense in sense_entities.senses:
        sense.id = f_sense_id_and_sense_id_map[sense.id]
    return sense_entities


@router.get("/search", response_model=DictionaryWordInfo)
async def search(query: str):
    return await dictionary_provider.search(query)


@router.patch("/public", status_code=status.HTTP_201_CREATED)
async def add_public_sense_to_user(
    add_scheme: SAddSenseRequest,
    user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_public_sense_to_user(db_session, user, add_scheme)


@router.patch("/personalize", status_code=status.HTTP_201_CREATED)
async def add_public_sense_to_user(
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


@router.delete("/{sense_id}")
async def delete_sense():
    pass
