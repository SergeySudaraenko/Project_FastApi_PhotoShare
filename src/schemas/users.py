from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from src.schemas.auth import Role

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

class RequestEmail(BaseModel):
    email: EmailStr

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=255)

class UserDbModel(BaseModel):
    uid: str
    username: str
    email: EmailStr
    avatar: Optional[str] = None
    role: Role
    created_at: datetime

class UserResponseSchema(BaseModel):
    user: UserDbModel

class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    avatar_url: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int  
    created_at: datetime
    updated_at: datetime
    role: Role|str
    confirmed: Optional[bool] = None
    is_active: bool

class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)

    class Config:
        orm_mode = True
