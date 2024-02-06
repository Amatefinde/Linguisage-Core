from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class DataBaseSettings(BaseSettings):
    host: str = os.environ.get("DB_HOST")
    port: str = os.environ.get("DB_PORT")
    db_name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    password: str = os.environ.get("DB_PASS")

    echo: bool = False
    url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


class Microservices(BaseSettings):
    LITERATURE_MS_URL: str
    DICTIONARY_MS_URL: str


class Auth(BaseSettings):
    RESET_PASSWORD_SECRET: str
    VERIFICATION_TOKEN_SECRET: str


class Email(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_SECRET: str


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    auth: Auth = Auth()
    db: DataBaseSettings = DataBaseSettings()
    ms: Microservices = Microservices()
    email: Email = Email()


settings = Settings()
