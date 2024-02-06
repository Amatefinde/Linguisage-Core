from fastapi import APIRouter
from .user_manager import fastapi_users, auth_backend
from .schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
