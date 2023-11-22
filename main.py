from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.datastructures import Headers
from starlette.requests import Request

from core.config import settings
from api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If there is no tables, then create it
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://192.168.31.23:3000",
    "http://93.81.252.160:8001",
    "http://93.81.252.160:7777",
    "http://93.81.252.160:7777/",
    "http://93.81.252.160:3000",
    "http://localhost:3000",
    "http://192.168.31.1:0000",
    "http://26.96.4.216:3000",
    "http://linguitest.ddns.net",
    "http://linguitest.ddns.net:7777",
]

headers = [
    "Authorization",
    "Content-Type",
    "Set-Cookie",
    "Accept",
    "Content-Length",
    "User-Agent",
    "Proxy-Authorization",
    "Proxy-Connection",
    "User-Agent",
    "Access-Control-Allow-Headers",
    "Access-Control-Request-Method",
    "Access-Control-Allow-Origin",
]

method = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]

app.include_router(router, prefix=settings.api_v1_prefix)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=headers,
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
