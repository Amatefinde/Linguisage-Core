from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.core.database.models import User, db_user_dependency
from src.api_v1 import router as api_v1_router

from src.api_v1.user.user_manager import (
    current_active_user_dependency,
)

app = FastAPI(title="Linguisage Core")
app.include_router(api_v1_router)

origins = [
    "http://localhost:5173",
    "http://192.168.31.23:5173",
    "http://linguisage.ru",
    "https://linguisage.ru",
    "https://linguisage.ru:8080",
    "https://linguisage.ru:55555",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",  # url_path
    StaticFiles(directory="/static"),  # path_to_directory
    name="/static_files",
)

# @app.on_event("startup")
# async def on_startup():
#     # Not needed if you setup a migration system like Alembic
#     await create_db_and_tables()
