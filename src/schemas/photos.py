from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.database.models import Tag, Comment, Rating


class PhotoBase(BaseModel):
    url: str
    description: Optional[str] = None


class PhotoCreate(PhotoBase):
    tags: Optional[List[str]] = None


class PhotoInDBBase(PhotoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    average_rating: float = 0.0

    class Config:
        orm_mode = True


class Photo(PhotoInDBBase):
    tags: List["Tag"] = []
    comments: List["Comment"] = []
    ratings: List["Rating"] = []


class PhotoURLResponse(BaseModel):
    url: str
    qr_code_url: str
