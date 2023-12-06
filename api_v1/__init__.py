from fastapi import APIRouter

from .user.views import router as user_router
from .literature.views import router as literature_router
from .word.views import router as word_router
from .word.crud import get_user_sense_by_f_id
from .training.views import router as training_router

router = APIRouter()
router.include_router(user_router)
router.include_router(literature_router)
router.include_router(word_router)
router.include_router(training_router)
