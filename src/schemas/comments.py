from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    photo_id: int


class CommentUpdate(BaseModel):
    comment_text: Optional[str] = None
    


class CommentInDBBase(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int
    is_deleted: bool  

    class Config:
        orm_mode = True


class Comment(CommentInDBBase):
    pass
