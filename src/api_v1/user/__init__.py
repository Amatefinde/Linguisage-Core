__all__ = ["router"]


from fastapi import APIRouter, Depends
from .user_manager import fastapi_users, auth_backend, current_active_user_dependency
from .schemas import UserCreate, UserRead, UserUpdate
from .views import router as views_router

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(views_router)
