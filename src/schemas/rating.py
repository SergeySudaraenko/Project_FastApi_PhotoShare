from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RatingBase(BaseModel):
    value: int = Field(..., description="The rating score between 1 and 5")


class RatingCreate(RatingBase):
    photo_id: Optional[int] = None


class RatingInDBBase(RatingBase):
    id: int
    user_id: int
    photo_id: int
    value: int

    model_config = ConfigDict(from_attributes=True)


class AverageRatingResponse(BaseModel):
    average_rating: float
