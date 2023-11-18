from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database import db_helper
from core.database.models import User, UserWordImage
from . import crud
from core.providers.neural_provider import get_meaning
from fastapi import Depends, APIRouter, HTTPException, status
from api_v1.user import get_current_user
import requests
from .utils import get_meanings_from_word_info
from .schemas import (
    MeaningResponseScheme,
    UserWordMeaningRequestScheme,
    UserWordMeaningScheme,
    LinkMeaningWithImagesScheme,
)

router = APIRouter(prefix="/words", tags=["Words"])


@router.get("/meaning")
async def get_meaning_for_word(word: str, context: str = None):
    get_word_endpoint_url = settings.content_manager_url + "/word/get"
    response = requests.get(
        get_word_endpoint_url,
        params={"word": word},
    )
    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not yet info about this world in db",
        )

    word_info = response.json()

    if context:
        meanings: list[str] = get_meanings_from_word_info(word_info)
        response_meaning = get_meaning(
            meanings=meanings, word=word_info["content"], context=context
        )
        word_info["current_meaning"] = response_meaning.meaning
    else:
        word_info["current_meaning"] = None

    return word_info


@router.post("/user/meanings", status_code=status.HTTP_201_CREATED)
async def add_meaning_to_user(
    user_word_meaning: UserWordMeaningRequestScheme,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    user_word_meaning = UserWordMeaningScheme(
        **user_word_meaning.model_dump(), user_id=current_user.id
    )

    return await crud.add_user_word_meaning(session, user_word_meaning)


@router.post(
    "/user/meanings/image",
    summary="Pair image to user meaning",
    status_code=status.HTTP_201_CREATED,
)
async def pair_image_to_user_meaning(
    image_id: int,
    user_meaning_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_user_meaning = await crud.get_user_meaning_by_id(
        session=session, user_meaning_id=user_meaning_id
    )
    if db_user_meaning:
        db_image_meaning = await crud.pair_image_to_user_word_meaning(
            session=session, image_id=image_id, user_word_meaning=db_user_meaning
        )
        return db_image_meaning
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User with this id not found"
    )


@router.get("user/meanings", summary="Get list of user meanings with photo")
async def get_list_of_user_meanings_with_img(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_user_meaning_with_img = await crud.get_list_of_meanings_with_img_by_user_id(
        session,
        current_user,
    )
    return db_user_meaning_with_img
