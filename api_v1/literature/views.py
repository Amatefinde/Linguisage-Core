from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.database.models import User, Literature
from . import crud
from core.database import db_helper
from api_v1.user import get_current_user
from core.providers import content_provider
from .schemas import LiteratureResponseScheme
from .dependencies import current_user_literature_by_id

router = APIRouter(prefix="/literature", tags=["Literature"])


@router.get(
    "/list",
    summary="Get list user literature by user_id",
    response_model=list[LiteratureResponseScheme],
)
async def get_literature(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_user_literature(session=session, user_id=current_user.id)


@router.get("/last")
async def get_last_opened_literature(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    db_literature = await crud.get_last_opened(session, current_user.id)
    if db_literature:
        literature_pages = await content_provider.get_literature_pages(
            db_literature.f_literature_id, 1, 1
        )
        setattr(db_literature, "cover", literature_pages[0]["img"])
        return db_literature
    return None


@router.post("/", response_model=LiteratureResponseScheme)
async def add_literature(
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
    use_ocr: bool = False,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    f_literature_id = await content_provider.add_literature(file.file, use_ocr)
    if f_literature_id:
        db_literature = await crud.add_literature_by_user_id(
            session=session,
            user_id=current_user.id,
            title=file.filename,
            f_literature_id=f_literature_id,
        )
        return db_literature

    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/")
async def get_literature_pages(
    start_page: int = 1,
    end_page: int = 0,
    literature_db: Literature = Depends(current_user_literature_by_id),
):
    literature_pages = await content_provider.get_literature_pages(
        literature_db.f_literature_id, start_page, end_page
    )
    return literature_pages


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_literature(
    literature_db=Depends(current_user_literature_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await content_provider.delete_literature(literature_db.f_literature_id)
    await crud.delete_literature(session=session, db_literature=literature_db)
