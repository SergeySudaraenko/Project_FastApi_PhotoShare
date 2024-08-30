from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship


# Pydantic Models
class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class TagInDBBase(TagBase):
    id: int

    class Config:
        orm_mode = True


class TagResponse(TagInDBBase):
    pass


class PhotoTagBase(BaseModel):
    photo_id: int
    tag_id: int


class PhotoTagCreate(PhotoTagBase):
    pass


class PhotoTagInDBBase(PhotoTagBase):
    class Config:
        orm_mode = True


class PhotoTagResponse(PhotoTagInDBBase):
    pass
