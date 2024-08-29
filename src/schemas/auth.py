from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import enum


class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class AuthBase(BaseModel):
    username: str
    email: EmailStr


class AuthCreate(AuthBase):
    password: str


class AuthInDBBase(AuthBase):
    id: int
    uid: str
    created_at: datetime
    updated_at: datetime
    role: Role
    confirmed: bool

    class Config:
        from_attributes = True


class Auth(AuthInDBBase):
    pass


class AuthUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    confirmed: Optional[bool] = None


class AuthToken(BaseModel):
    access_token: str
    token_type: str