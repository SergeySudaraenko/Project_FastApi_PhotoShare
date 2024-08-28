from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/ProjectDB"
    SECRET_KEY_JWT: str = "1234567890"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "postgresmail.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: str = "postgres"
    MAIL_PORT: int = 567234
    MAIL_SERVER: str = "postgres"
    # REDIS_DOMAIN: str = "localhost"
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str = None
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v


    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8") #noqa

settings = Settings()


# MAIL_USERNAME=hw2024@meta.ua
# MAIL_PASSWORD=Lehfrb13579
# MAIL_FROM=hw2024@meta.ua