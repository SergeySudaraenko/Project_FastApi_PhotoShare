from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.auth import AuthInDBBase, Role


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserDbModel(BaseModel):
    uid: str
    username: str
    email: EmailStr
    avatar: str
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponseSchema(UserBase):
    user: UserDbModel


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    avatar_url: Optional[str]

    class Config:
        orm_mode = True
