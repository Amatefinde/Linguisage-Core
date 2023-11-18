from fastapi import APIRouter

from .user.views import router as user_router
from .literature.views import router as literature_router
from .word.views import router as word_router


router = APIRouter()
router.include_router(user_router)
router.include_router(literature_router)
router.include_router(word_router)
