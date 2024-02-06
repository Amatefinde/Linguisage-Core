from fastapi import APIRouter

from .user import router as auth_router
from .literature import router as literature_router
from src.core import settings

router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(auth_router)
router.include_router(literature_router)

__all__ = ["router"]
