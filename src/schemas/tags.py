from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database.db import Base

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

# SQLAlchemy Models
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(50), unique=True, index=True)
    
   
    photos = relationship("Photo", secondary="photo_tags", back_populates="tags")

class PhotoTag(Base):
    __tablename__ = 'photo_tags'

    photo_id = Column(Integer, ForeignKey('photos.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    photo = relationship("Photo", back_populates="tags")
    tag = relationship("Tag", back_populates="photos")

class Photo(Base):
    __tablename__ = 'photos'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), unique=True, index=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Связи
    owner = relationship("User", backref="photos")
    tags = relationship("Tag", secondary="photo_tags", back_populates="photos")
    comments = relationship("Comment", back_populates="photo")
    ratings = relationship("Rating", back_populates="photo")
