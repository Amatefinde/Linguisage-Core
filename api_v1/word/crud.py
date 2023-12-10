import asyncio
from sqlalchemy import select
from core.providers import dictionary_provider
from .schemas import SPairUserAndSense, SenseWithImagesDTO
from core.database.models import Sense, Image, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


async def pair_user_and_sense(
    session: AsyncSession,
    s_pair_user_and_sense: SPairUserAndSense,
    user: User,
):
    db_sense = Sense(
        user=user,
        f_sense_id=s_pair_user_and_sense.f_sense_id,
        literature_id=s_pair_user_and_sense.literature_id,
        status=s_pair_user_and_sense.status,
    )
    db_sense.images = [
        Image(f_img_id=f_img_id) for f_img_id in s_pair_user_and_sense.f_images_id
    ]
    session.add(db_sense)
    await session.commit()
    await session.refresh(db_sense)

    return db_sense


async def _get_db_user_senses(session: AsyncSession, user: User):
    stmt = select(Sense).where(Sense.user == user).options(selectinload(Sense.images))
    response = await session.execute(stmt)
    return response.scalars().all()


async def _get_senses_with_images_from_dictionary(senses_db):
    senses_from_dictionary_tasks = []
    for sense in senses_db:
        sense_dto = SenseWithImagesDTO.model_validate(sense)
        senses_from_dictionary_tasks.append(
            dictionary_provider.get_sense_with_images(sense_dto)
        )
    return await asyncio.gather(*senses_from_dictionary_tasks)


async def get_user_senses(
    session: AsyncSession, user: User
) -> tuple[dictionary_provider.SSenseP]:
    senses_db = await _get_db_user_senses(session, user)
    return await _get_senses_with_images_from_dictionary(senses_db)


async def get_user_sense_by_f_id(
    session: AsyncSession,
    f_sense_id: int,
) -> Sense:
    stmt = select(Sense).where(Sense.f_sense_id == f_sense_id)
    db_response = await session.execute(stmt)
    return db_response.scalar_one()


async def get_user_sense_by_f_id_with_f_images_id(
    session: AsyncSession,
    f_sense_id: int,
) -> Sense:
    stmt = (
        select(Sense)
        .where(Sense.f_sense_id == f_sense_id)
        .options(selectinload(Sense.images))
    )
    db_response = await session.execute(stmt)
    return db_response.scalar_one()


async def set_images_for_user_sense(
    session: AsyncSession,
    sense_db: Sense,
    f_images_id: list[int],
) -> Sense:
    sense_db.images = [
        Image(f_img_id=f_image_id, sense_id=sense_db.id) for f_image_id in f_images_id
    ]
    await session.commit()
    await session.refresh(sense_db)
    return sense_db


async def delete_user_sense(
    session: AsyncSession,
    sense_db: Sense,
) -> None:
    await session.delete(sense_db)
    await session.commit()
