from typing import Iterable

from loguru import logger
from sqlalchemy import select, Sequence, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.database.models import Answer, User, Sense
from .schemas import AnswerRequest
from src.core.providers.Dictionary.schemas.get_senses import SGetSense


async def add_answer(session: AsyncSession, user: User, answer: AnswerRequest) -> Answer:
    answer = Answer(**answer.model_dump(), user=user)
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer


async def get_user_senses_with_answers(session: AsyncSession, user: User) -> Sequence[Sense]:
    stmt = (
        select(Sense)
        .options(
            selectinload(Sense.answers),
            selectinload(Sense.sense_images),
            selectinload(Sense.word_images),
        )
        .where(Sense.user == user)
        .where(Sense.status == "in_process")
    )

    return (await session.scalars(stmt)).all()
