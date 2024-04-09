from types import NoneType
from typing import Sequence

from loguru import logger
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .scheme.request import SAddSenseRequest
from src.core.database.models import User, SenseImage, Sense, WordImage
from src.core.providers.Dictionary.schemas.general import (
    PersonalizeSenseEntity,
    DictionaryWordInfo,
)
from ...core.providers.Dictionary.schemas.get_senses import SGetSense
from src.core.types import sense_status_type


async def check_is_user_have_sense_by_f_sense_id(
    session: AsyncSession, user: User, f_sense_id: int
) -> bool:
    stmt = select(Sense).where(Sense.f_sense_id == f_sense_id).where(Sense.user == user)
    row_response = await session.execute(stmt)
    # logger.debug(row_response.scalar())
    return bool(row_response.scalar_one_or_none())


async def add_public_sense_to_user(
    session: AsyncSession,
    user: User,
    add_scheme: SAddSenseRequest,
) -> Sense:
    db_word_images = [WordImage(f_img_id=f_img_id) for f_img_id in add_scheme.f_word_image_ids]
    db_sense_images = [SenseImage(f_img_id=f_img_id) for f_img_id in add_scheme.f_sense_image_ids]
    db_sense = Sense(
        f_sense_id=add_scheme.f_sense_id,
        word_images=db_word_images,
        sense_images=db_sense_images,
        user=user,
    )
    session.add(db_sense)
    await session.commit()
    await session.refresh(db_sense)
    return db_sense


async def add_personalize_sense_to_user(
    session: AsyncSession,
    user: User,
    personalize_sense_entity: PersonalizeSenseEntity,
    literature_id: int | None = None,
) -> Sense:
    db_sense_images = [
        SenseImage(f_img_id=img.f_img_id) for img in personalize_sense_entity.sense_images
    ]
    db_sense = Sense(
        f_sense_id=personalize_sense_entity.f_sense_id,
        sense_images=db_sense_images,
        user=user,
        literature_id=literature_id,
    )
    session.add(db_sense)
    await session.commit()
    await session.refresh(db_sense)
    return db_sense


async def get_senses(
    session: AsyncSession,
    user: User,
    new_first: bool | None = None,
    page: int | None = None,
    limit: int | None = None,
    status: sense_status_type | None = None,
) -> list[SGetSense]:
    stmt = (
        select(Sense)
        .where(Sense.user == user)
        .options(
            selectinload(Sense.sense_images),
            selectinload(Sense.word_images),
        )
    )
    if page is not None:
        stmt = stmt.offset(page - 1)
    if limit is not None:
        stmt = stmt.limit(limit)
    if status is not None:
        stmt = stmt.where(Sense.status == status)
    if new_first is not None:
        stmt = stmt.order_by(desc(Sense.created_at) if new_first else Sense.created_at)

    row_response = (await session.scalars(stmt)).all()
    result = [SGetSense.model_validate(x, from_attributes=True) for x in row_response]
    return result


def __mark_already_added_senses(
    dictionary_word_info: DictionaryWordInfo, added_senses: Sequence[Sense]
):
    for already_added_sense in added_senses:
        for word_sense in dictionary_word_info.senses:
            if word_sense.f_sense_id == already_added_sense.f_sense_id:
                setattr(word_sense, "in_user_dictionary", True)


async def mark_senses_that_user_already_have(
    session: AsyncSession,
    user: User,
    dictionary_word_info: DictionaryWordInfo,
) -> None:
    f_sense_ids_for_word: list[int] = [sense.f_sense_id for sense in dictionary_word_info.senses]
    stmt = (
        select(Sense).where(Sense.user == user).where(Sense.f_sense_id.in_(f_sense_ids_for_word))
    )
    row_response = await session.execute(stmt)
    already_added_senses = row_response.scalars().all()
    __mark_already_added_senses(dictionary_word_info, already_added_senses)


async def get_sense(session: AsyncSession, sense_id: int) -> Sense | None:
    return await session.get(Sense, sense_id)


async def set_sense_status(
    session: AsyncSession,
    sense: Sense,
    status: sense_status_type,
) -> Sense:
    sense.status = status
    await session.commit()
    await session.refresh(sense)
    return sense
