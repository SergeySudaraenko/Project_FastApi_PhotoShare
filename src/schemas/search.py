from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int


class PhotoBase(BaseModel):
    description: Optional[str] = None
    tags: Optional[List[str]] = []

    model_config = ConfigDict(from_attributes=True)


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class Photo(PhotoBase):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    rating: Optional[float] = None


class PhotoSearchParams(BaseModel):
    keyword: Optional[str] = None
    tag: Optional[str] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class PhotoRating(BaseModel):
    photo_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True)


class PhotoRatingUpdate(PhotoRating):
    pass


class CommentBase(BaseModel):
    text: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int
    photo_id: int


class UserProfile(BaseModel):
    username: str
    full_name: str
    email: str
    registered_at: datetime
    photo_count: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SearchFilters(BaseModel):
    keyword: Optional[str] = None
    tags: Optional[List[str]] = None
    min_rating: Optional[int] = None
    max_rating: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SearchResponse(BaseModel):
    id: int
    url: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    tags: List[str] = []
    average_rating: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
