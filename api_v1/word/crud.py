from sqlalchemy import Select
from core.providers import content_provider
from .schemas import SPairUserAndSense
from core.database.models import Sense, Image, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from core.config import settings


async def pair_user_and_sense(
    session: AsyncSession, s_pair_user_and_sense: SPairUserAndSense, user: User
):
    db_sense = Sense(**s_pair_user_and_sense.model_dump(exclude_defaults=True))
    db_sense.user = user
    session.add(db_sense)
    await session.commit()
    await session.refresh(db_sense)
    return db_sense


#
# async def get_user_meaning_by_id(
#     session: AsyncSession, user_meaning_id: int
# ) -> UserWordMeaning | None:
#     return await session.get(UserWordMeaning, user_meaning_id)
#
#
# async def pair_image_to_user_word_meaning(
#     session: AsyncSession,
#     image_id: int,
#     user_word_meaning: UserWordMeaning,
# ):
#     db_user_word_image = UserWordImage(
#         content=image_id, user_word_meaning=user_word_meaning
#     )
#     session.add(db_user_word_image)
#     await session.commit()
#
#
# async def get_list_of_meanings_with_img_by_user_id(
#     session: AsyncSession,
#     user: User,
# ):
#     stmt = (
#         Select(User)
#         .options(joinedload(User.words).options(joinedload(UserWordMeaning.images)))
#         .filter(User.id == user.id)
#     )
#     result = await session.scalar(stmt)
#
#     user_meanings = []
#
#     for meaning_with_image in result.words:
#         meaning_with_image = LinkMeaningWithImagesScheme(**meaning_with_image.__dict__)
#
#         images = []
#         for image_id in meaning_with_image.images:
#             img_url = (
#                 settings.content_manager_url
#                 + "/static/images"
#                 + content_provider.get_image_by_id(image_id.content).strip('"')
#             )
#             images.append(img_url)
#
#         meaning_with_image = meaning_with_image.model_dump()
#
#         row_word_meaning = content_provider.get_word_meaning(
#             meaning_with_image["content"]
#         )
#
#         meaning_with_image["content"] = UserWordMeaningResponseScheme(
#             meaning=row_word_meaning["meaning"],
#             short_meaning=row_word_meaning["short_meaning"],
#             word=row_word_meaning["word"]["content"],
#         )
#         meaning_with_image["images"] = images
#
#         user_meanings.append(meaning_with_image)
#
#     return user_meanings
