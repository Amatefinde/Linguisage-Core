from loguru import logger
from sqlalchemy import select
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


async def get_user_answers(session: AsyncSession, senses: list[SGetSense]):
    stmt = (
        select(Sense)
        .options(selectinload(Sense.answers))
        .where(Sense.id.in_([sense.id for sense in senses]))
    )
    row_db_senses_with_answer = await session.execute(stmt)
    db_senses_with_answer = row_db_senses_with_answer.scalars().all()
    for sense in db_senses_with_answer:
        for answer in sense.answers:
            logger.debug(answer)
