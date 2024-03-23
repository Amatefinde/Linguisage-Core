from fastapi import APIRouter, Depends, status, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.user_manager import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import User, Sense
from src.core.providers.Dictionary import dictionary_provider
import src.api_v1.sense.crud as sense_crud


router = APIRouter(tags=["Training"], prefix="/training")


@router.get("")
async def get_training(
    exercise_number: int = 10,
    db_session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_active_user_dependency),
):
    senses_in_process = await sense_crud.get_senses(
        db_session, user, status="in_process", limit=exercise_number
    )
    logger.debug(len(senses_in_process))
    senses_in_queue = []
    if len(senses_in_process) < exercise_number:
        require_sense_in_queue: int = exercise_number - len(senses_in_process)
        logger.debug(f"require_sense_in_queue: {require_sense_in_queue}")
        senses_in_queue = await sense_crud.get_senses(
            db_session, user, status="in_queue", limit=require_sense_in_queue
        )

    picked_senses = senses_in_process + senses_in_queue
    sense_with_content = await dictionary_provider.get_senses(picked_senses)
    return sense_with_content
