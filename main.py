from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from core.config import settings
from api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If there is no tables, then create it
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix=settings.api_v1_prefix)
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://192.168.31.23:7210",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
