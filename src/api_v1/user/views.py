from fastapi import APIRouter, Depends
from src.api_v1.user.user_manager import current_active_user_dependency
from src.api_v1.user.schemas import UserRead
from src.core.database.models import User

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def read_me(
    user: User = Depends(current_active_user_dependency),
):
    return user
