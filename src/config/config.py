from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_DB = "koyebdb"
    PG_USER = "koyeb-adm"
    PG_PASSWORD = "v6sNjAnxio5q"
    PG_PORT = "5432"
    PG_DOMAIN = "ep-delicate-credit-a285zbki.eu-central-1.pg.koyeb.app"
    DB_URL = f"postgresql+asyncpg://${PG_USER}:${PG_PASSWORD}@${PG_DOMAIN}:${PG_PORT}/${PG_DB}"
    SECRET_KEY_JWT = 1234567890
    ALGORITHM = "HS256"
    MAIL_USERNAME = "vlad_bb@meta.ua"
    MAIL_PASSWORD = "tQM2JULusy"
    MAIL_FROM = "vlad_bb@meta.ua"
    MAIL_PORT = 465
    MAIL_SERVER = "smtp.meta.ua"
    CLOUDINARY_NAME = "dpc5fcmq5"
    CLOUDINARY_API_KEY = 951437173691459
    CLOUDINARY_API_SECRET = "6irfVmNhHCvEDnMjaGy4DRSjcpk"

    @classmethod
    @field_validator("ALGORITHM")
    def validate_algorithm(cls, v):
        if v not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")  # noqa


settings = Settings()
