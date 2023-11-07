from contextlib import asynccontextmanager
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from fastapi import FastAPI
import uvicorn
from core.config import settings

from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If there is no tables, then create it
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
