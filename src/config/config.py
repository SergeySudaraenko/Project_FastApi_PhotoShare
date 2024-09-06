from pydantic import  field_validator, ConfigDict
from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    PG_DB: str = "koyebdb"
    PG_USER: str = "koyeb-adm"
    PG_PASSWORD: str = "v6sNjAnxio5q"
    PG_PORT: str = "5432"
    PG_DOMAIN: str = "ep-delicate-credit-a285zbki.eu-central-1.pg.koyeb.app"
    
    SECRET_KEY_JWT: int = 1234567890
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "vlad_bb@meta.ua"
    MAIL_PASSWORD: str = "tQM2JULusy"
    MAIL_FROM: str = "vlad_bb@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    CLOUDINARY_NAME: str = "dpc5fcmq5"
    CLOUDINARY_API_KEY: int = 951437173691459
    CLOUDINARY_API_SECRET: str = "6irfVmNhHCvEDnMjaGy4DRSjcpk"
    
    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_DOMAIN}:{self.PG_PORT}/{self.PG_DB}"

    @classmethod
    @field_validator("ALGORITHM")
    def validate_algorithm(cls, v):
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

settings = Settings()

