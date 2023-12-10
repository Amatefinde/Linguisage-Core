from typing import Annotated
from api_v1.user import get_current_user
from core.providers.Dictionary import get_word_by_query, WordDTO
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import db_helper
from core.database.models import User, Image, Sense
from . import crud
from .schemas import SPairUserAndSense, SenseWithImagesDTO, SPairSenseAndImages
from fastapi import Depends, APIRouter, HTTPException, status
from api_v1 import train_logic


router = APIRouter(prefix="/words", tags=["Words"])


@router.get("/senses", response_model=WordDTO)
async def get_meaning_for_word(
    query: str,
    download_if_not_found: bool = True,
    context: str = None,
):
    sense: WordDTO | None = await get_word_by_query(query, download_if_not_found)
    if sense:
        sense.current_sense_id = sense.senses[0].id  # todo
        return sense
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    r"/users/senses",
    status_code=status.HTTP_201_CREATED,
    summary="Add sense to user dictionary",
)
async def add_meaning_to_user(
    s_pair_user_and_sense: SPairUserAndSense,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_sense: Sense = await crud.pair_user_and_sense(
        session, s_pair_user_and_sense, user
    )
    return db_sense


#
#
# @router.post(
#     "/users/sense/image",
#     summary="Pair image to user sense",
#     status_code=status.HTTP_201_CREATED,
# )
# async def pair_image_to_user_meaning(
#     image_id: int,
#     user_meaning_id: int,
#     current_user: Annotated[User, Depends(get_current_user)],
#     session: AsyncSession = Depends(db_helper.session_dependency),
# ):
#     db_user_meaning = await crud.get_user_meaning_by_id(
#         session=session, user_meaning_id=user_meaning_id
#     )
#     if db_user_meaning:
#         db_image_meaning = await crud.pair_image_to_user_word_meaning(
#             session=session, image_id=image_id, user_word_meaning=db_user_meaning
#         )
#         return db_image_meaning
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail="User with this id not found"
#     )
#
#
@router.get("/users/senses", summary="Get list of user senses with images")
async def get_user_senses(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_user_senses_with_images = await crud.get_user_senses(
        session,
        current_user,
    )
    for sense in db_user_senses_with_images:
        score_and_status = await train_logic.get_score_and_status_by_f_sense_id(
            session, sense.f_sense_id
        )
        sense.score = score_and_status.score
        sense.status = score_and_status.status
    return db_user_senses_with_images


@router.put("/users/senses/images", summary="Set images for user sense")
async def set_images_for_user_sense(
    sense: SPairSenseAndImages,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        sense_db: Sense = await crud.get_user_sense_by_f_id_with_f_images_id(
            session, sense.f_sense_id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sense with id {sense.f_sense_id} not found",
        )
    if sense_db.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await crud.set_images_for_user_sense(session, sense_db, sense.f_images_id)


@router.delete("/users/senses", summary="Set images for user sense")
async def set_images_for_user_sense(
    f_sense_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    try:
        sense_db: Sense = await crud.get_user_sense_by_f_id_with_f_images_id(
            session, f_sense_id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sense with id {f_sense_id} not found",
        )
    if sense_db.user != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await crud.delete_user_sense(session, sense_db)
