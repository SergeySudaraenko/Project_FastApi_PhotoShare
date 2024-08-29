from pydantic import BaseModel, Field
from typing import List, Optional

class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

class PhotoBase(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    url: str
    created_at: str
    updated_at: str
    user_id: int
    rating: Optional[float] = None

class PhotoSearchParams(BaseModel):
    keyword: Optional[str] = None
    tag: Optional[str] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class PhotoRating(BaseModel):
    photo_id: int
    rating: int

    class Config:
        from_attributes = True

class PhotoRatingUpdate(PhotoRating):
    pass

class CommentBase(BaseModel):
    text: str

    class Config:
        from_attributes = True

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: str
    updated_at: str
    user_id: int
    photo_id: int

class UserProfile(BaseModel):
    username: str
    full_name: str
    email: str
    registered_at: str
    photo_count: int

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
