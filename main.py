from fastapi import Depends, FastAPI

from src.core.database.models import User, db_user_dependency
from src.api_v1 import router as api_v1_router

from src.api_v1.user.user_manager import (
    current_active_user_dependency,
)

app = FastAPI(title="Linguisage Core")
app.include_router(api_v1_router)


# @app.on_event("startup")
# async def on_startup():
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()
