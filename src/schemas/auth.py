import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class AuthBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
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

    model_config = ConfigDict(from_attributes=True)


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


class TokenData(BaseModel):
    username: str
    role: Role
