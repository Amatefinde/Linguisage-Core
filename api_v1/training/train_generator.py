from typing import Literal

from .scemas import AnswerDTO, SenseDTO
from .crud import get_senses_for_user, set_sense_completed, set_sense_status
from core.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.word.schemas import SenseWithImagesDTO
from core.providers import dictionary_provider


async def define_mastered_senses(session: AsyncSession, user: User):
    f_senses_in_process: list[SenseDTO] = await get_senses_for_user(
        session,
        user,
        status="in_process",
    )
    completed: list[SenseDTO] = []
    for sense in f_senses_in_process:
        sense_score = 0
        for answer in sense.answers:
            if answer.is_correct:
                sense_score += 0.25
            else:
                sense_score -= 0.1
        if sense_score >= 1:
            await set_sense_completed(session, sense.f_sense_id)
            completed.append(sense)
        print(sense, sense_score)
    return completed


async def _pick_senses_for_mastering_from_queue(
    session: AsyncSession,
    user: User,
    number: int,
):
    f_sense_id_in_queue: list[SenseDTO] = await get_senses_for_user(
        session, user, status="in_queue"
    )
    return f_sense_id_in_queue[:number]


async def _set_status_for_sequence_senses(
    session: AsyncSession,
    senses: list[SenseDTO],
    status: Literal["complete", "in_process", "in_queue"],
):
    for sense in senses:
        await set_sense_status(session, sense.f_sense_id, status)


async def _get_senses_for_training(
    session: AsyncSession, user: User, number: int
) -> list[SenseDTO]:
    senses_in_process: list[SenseDTO] = await get_senses_for_user(
        session,
        user,
        status="in_process",
    )
    if (senses_not_enough := number - len(senses_in_process)) > 0:
        senses_from_queue = await _pick_senses_for_mastering_from_queue(
            session, user, senses_not_enough
        )
        await _set_status_for_sequence_senses(session, senses_from_queue, "in_process")
        return senses_from_queue + senses_in_process
    else:
        picked_senses = senses_in_process[:number]
        await _set_status_for_sequence_senses(session, picked_senses, "in_process")
        return picked_senses


async def _set_row_examples_hidden_word(
    senses: list[dictionary_provider.SSenseP],
) -> list[dictionary_provider.SSenseP]:
    for sense in senses:
        word = sense.word.word
        for row_example in sense.row_examples:
            row_example_hidden_word = row_example.model_copy()
            row_example_hidden_word.row_example = (
                row_example_hidden_word.row_example.replace(word, "_" * len(word))
            )
            sense.row_examples_hidden_word.append(row_example_hidden_word)
    return senses


async def generate(
    session: AsyncSession, user: User, number: int
) -> list[dictionary_provider.SSenseP]:
    senses_for_training: list[SenseDTO] = await _get_senses_for_training(
        session, user, number
    )
    sense_ready_for_send_to_dictionary = [
        SenseWithImagesDTO.model_validate(sense) for sense in senses_for_training
    ]
    senses: list[
        dictionary_provider.SSenseP
    ] = await dictionary_provider.get_senses_with_images(
        sense_ready_for_send_to_dictionary
    )
    return await _set_row_examples_hidden_word(senses)
