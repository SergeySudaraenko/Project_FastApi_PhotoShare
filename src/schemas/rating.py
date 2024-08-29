from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class RatingBase(BaseModel):
    score: Decimal

    @classmethod
    def validate_score(cls, score: Decimal) -> Decimal:
        if not (0 < score < 6):
            raise ValueError('Score must be greater than 0 and less than 6.')
        return score

class RatingCreate(RatingBase):
    pass

class RatingInDBBase(RatingBase):
    id: int
    user_id: int
    photo_id: int

    class Config:
        from_attributes = True

class Rating(RatingInDBBase):
    pass
