from core.database.models import Sense, Answer, User
from sqlalchemy.ext.asyncio import AsyncSession
from .scemas import SAnswer, SenseDTO
from api_v1 import get_user_sense_by_f_id
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence, Literal


async def add_answer(session: AsyncSession, user: User, answer: SAnswer):
    db_sense: Sense = await get_user_sense_by_f_id(session, answer.f_sense_id)
    session.add(Answer(user_id=user.id, is_correct=answer.is_correct, sense_id=db_sense.id))
    await session.commit()


async def set_sense_completed(session: AsyncSession, f_sense_id: int):
    db_sense = await get_user_sense_by_f_id(session, f_sense_id)
    db_sense.status = "complete"
    await session.commit()


async def set_sense_status(
    session: AsyncSession,
    f_sense_id: int,
    status: Literal["complete", "in_process", "in_queue"],
):
    db_sense = await get_user_sense_by_f_id(session, f_sense_id)
    db_sense.status = status
    await session.commit()


async def get_senses_for_user(
    session: AsyncSession,
    user: User,
    status: Literal["complete", "in_process", "in_queue", "all"] = "all",
) -> list[SenseDTO]:
    stmt = (
        select(Sense)
        .where(Sense.user == user)
        .options(selectinload(Sense.answers))
        .options(selectinload(Sense.images))
    )
    if status != "all":
        stmt = stmt.where(Sense.status == status)
    response_db = await session.execute(stmt.order_by(Sense.created_at))
    senses: Sequence = response_db.scalars().all()
    return [SenseDTO.model_validate(sense) for sense in senses]
