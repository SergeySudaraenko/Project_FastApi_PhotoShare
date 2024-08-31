from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from src.database.models import Tag, Comment, Rating
from src.schemas.tags import TagResponse


class PhotoCreate(BaseModel):
    url: str
    description: Optional[str] = None
    owner_id: int


class PhotoResponse(BaseModel):
    id: int
    url: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
