from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.database.models import Sense
from typing import NamedTuple, Literal, Sequence
from sqlalchemy.ext.asyncio import AsyncSession


class ScoreAndStatus(NamedTuple):
    score: float
    status: Literal["complete", "in_process", "in_queue"]


async def calculate_score_by_sense_with_answers(
    sense_with_answers: Sequence,
) -> float:
    score = 0

    for sense_with_answer in sense_with_answers[0].answers:
        if sense_with_answer.is_correct:
            score += 0.25
        else:
            score -= 0.1
    return score


async def get_score_and_status_by_f_sense_id(
    session: AsyncSession,
    f_sense_id,
) -> ScoreAndStatus:
    stmt = (
        select(Sense)
        .where(Sense.f_sense_id == f_sense_id)
        .options(selectinload(Sense.answers))
    )
    db_response = await session.execute(stmt)
    sense_with_ans = db_response.scalars().all()
    status = sense_with_ans[0].status

    if status == "in_process":
        score = await calculate_score_by_sense_with_answers(sense_with_ans)
    elif status == "complete":
        score = 1
    else:
        score = 0
    return ScoreAndStatus(score=score, status=status)
