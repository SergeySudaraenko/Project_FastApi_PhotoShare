from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(BaseModel):
    photo_id: int
    content: str


class CommentUpdateSchema(BaseModel):
    comment_text: Optional[str] = None
    updated_at: datetime


class CommentInDBBase(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    comment_text: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentDelete(BaseModel):
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
