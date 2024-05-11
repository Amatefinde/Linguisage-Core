from typing import Annotated, Iterable

from fastapi import APIRouter, Depends, UploadFile, Form, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.user.user_manager import current_active_user_dependency
from src.core.database import db_helper
from src.core.database.models import User, Literature
from src.core.providers.Literature import literature_provider
from . import crud
from src.core.providers.Literature.scheme import (
    LiteratureEpubEntity,
    ManyLiteratureEpubEntity,
    SPatchRequest,
    LiteratureEpubEntityWithStats,
)
from .dependencies import literature_dependency

router = APIRouter(prefix="/literature", tags=["Literature"])


@router.get("", response_model=ManyLiteratureEpubEntity)
async def get_all_literature(
    current_user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_literature: Iterable[Literature] = await crud.get_all_user_literature(db_session, current_user)
    f_id_and_id_map = {literature.f_literature_id: literature.id for literature in db_literature}
    literature_entity = await literature_provider.get_many_book(list(f_id_and_id_map.keys()))
    for literature in literature_entity.books:
        literature.id = f_id_and_id_map[literature.id]
    return literature_entity


@router.post("")
async def add_literature(
    book: UploadFile,
    filename: Annotated[str, Form()],
    current_user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    book_entity: LiteratureEpubEntity = await literature_provider.add_book(book, filename)
    db_literature = await crud.add_user_literature(db_session, current_user, book_entity)
    return db_literature


@router.delete("/{literature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_literature(
    db_literature: Literature = Depends(literature_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    await literature_provider.delete_book(db_literature.f_literature_id)
    await crud.delete_literature(db_session, db_literature)


@router.patch("/{literature_id}", response_model=LiteratureEpubEntity)
async def update_literature(
    patch: SPatchRequest,
    db_literature: Literature = Depends(literature_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.patch_literature(db_session, db_literature, patch)
    epub_entity = await literature_provider.patch_book(db_literature.f_literature_id, patch)
    epub_entity.id = db_literature.id
    return epub_entity


@router.get("/last", response_model=LiteratureEpubEntityWithStats)
async def get_last_opened_literature(
    current_user: User = Depends(current_active_user_dependency),
    db_session: AsyncSession = Depends(db_helper.session_dependency),
):
    if db_literature := await crud.get_last_user_literature(db_session, user=current_user):
        literature: LiteratureEpubEntity = await literature_provider.get_one_book(
            db_literature.f_literature_id
        )
        stats = await crud.get_literature_stats(db_session, db_literature)
        return LiteratureEpubEntityWithStats(**literature.model_dump(), stats=stats)
    raise HTTPException(status_code=404, detail=f"User have not yet literature")
