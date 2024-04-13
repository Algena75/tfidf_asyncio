import os
from pydantic_settings import BaseSettings
import string
from fastapi.templating import Jinja2Templates


class Settings(BaseSettings):
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD :str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str | int = os.getenv("POSTGRES_PORT",5432)
    POSTGRES_DB : str = os.getenv("POSTGRES_DB","tdd")
    DATABASE_URL : str = (f"postgresql+asyncpg://{POSTGRES_USER}:"
                         f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
                         f"{POSTGRES_PORT}/{POSTGRES_DB}")

    class Config:
        env_file = '.env'


settings = Settings()

ARRAY = string.ascii_letters + string.digits
UPLOAD_TO = 'app/files/'
templates = Jinja2Templates(directory="app/templates")
