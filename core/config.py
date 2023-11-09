from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class AuthSettings:
    JWT_ACCESS_KEY: str = os.environ.get("JWT_ACCESS_KEY")
    JWT_REFRESH_KEY: str = os.environ.get("JWT_REFRESH_KEY")


class Settings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")

    db_url: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    db_echo: bool = False

    api_v1_prefix: str = "/api/v1"

    auth_settings: AuthSettings = AuthSettings()


settings = Settings()
