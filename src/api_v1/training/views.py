from math import floor

from fastapi import APIRouter, Depends, status, HTTPException, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.user_manager import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import User, Sense, Answer
from .schemas import AnswerRequest
from . import crud
from src.core.providers.Dictionary import dictionary_provider
from src.core.providers.Dictionary.schemas.get_senses import SGetSense
import src.api_v1.sense.crud as sense_crud
from src.core.providers.AI import SenseReview, RequestSenseReview, AI_provider

router = APIRouter(tags=["Training"], prefix="/training")


@router.get("")
async def get_training(
    total_amount_of_words: int = 10,
    percent_of_studied_words: int = Query(10, ge=0, le=100),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    amount_of_studied_words = floor(total_amount_of_words * (percent_of_studied_words / 100))
    amount_of_words_in_study = total_amount_of_words - amount_of_studied_words

    studied_senses = await sense_crud.get_senses(
        db_session, user, status="complete", limit=amount_of_studied_words
    )

    senses_in_process = await sense_crud.get_senses(
        db_session,
        user,
        status="in_process",
        limit=amount_of_words_in_study + (amount_of_studied_words - len(studied_senses)),
    )
    senses_in_queue = []

    if len(senses_in_process) < amount_of_words_in_study + (
        amount_of_studied_words - len(studied_senses)
    ):
        require_sense_in_queue: int = total_amount_of_words - len(senses_in_process)
        senses_in_queue = await sense_crud.get_senses(
            db_session, user, status="in_queue", limit=require_sense_in_queue
        )
    picked_senses: list[SGetSense] = senses_in_process + senses_in_queue + studied_senses
    sense_with_content = await dictionary_provider.get_senses(picked_senses)
    return sense_with_content


@router.post("/answer", status_code=status.HTTP_201_CREATED)
async def add_answer(
    user_answer: AnswerRequest,
    user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    sense_db = await sense_crud.get_sense(db_session, user_answer.sense_id)
    await sense_crud.set_sense_status(db_session, sense_db, "in_process")
    return await crud.add_answer(db_session, user, user_answer)


@router.post("/calculate")
async def calculate(
    db_session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    senses_with_answers = await crud.get_user_senses_with_answers(db_session, user)

    for sense in senses_with_answers:
        sense_score = 0
        for answer in sense.answers:
            if answer.is_correct:
                sense_score += 0.20
            else:
                sense_score -= 0.20
                sense_score = max(sense_score, 0)
        if sense_score > 1:
            sense.status = "complete"
            await db_session.commit()
            await db_session.refresh(sense)
            logger.debug(sense.id)


@router.post("/review", response_model=SenseReview)
async def review(request: RequestSenseReview):
    return AI_provider.review(request)
