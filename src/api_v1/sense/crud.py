from types import NoneType

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .scheme.request import SAddSenseRequest
from src.core.database.models import User, SenseImage, Sense, WordImage
from src.core.providers.Dictionary.schemas.general import PersonalizeSenseEntity
from ...core.providers.Dictionary.schemas.get_senses import SGetSense


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
    page: int | None = None,
    size: int | None = None,
) -> list[SGetSense]:
    if type(page) is not type(size):
        raise TypeError("Page and size must be a same type")
    if type(page) not in (NoneType, int):
        raise TypeError("Page must be of type int or NoneType")
    if type(page) is int and page < 1:
        raise ValueError("Page can't be less than 1")
    stmt = (
        select(Sense)
        .where(Sense.user == user)
        .options(
            selectinload(Sense.sense_images),
            selectinload(Sense.word_images),
        )
    )
    if page:
        stmt.offset(page - 1).limit(size)

    row_response = (await session.scalars(stmt)).all()
    return [SGetSense.model_validate(x, from_attributes=True) for x in row_response]