from pydantic import BaseModel, Field, validator, ConfigDict
from decimal import Decimal
from typing import Optional


class RatingBase(BaseModel):
    score: Decimal = Field(..., description="The rating score between 0 and 6")

    @validator('score')
    def validate_score(cls, score: Decimal) -> Decimal:
        if not (0 < score < 6):
            raise ValueError('Score must be greater than 0 and less than 6.')
        return score


class RatingCreate(RatingBase):
    photo_id: Optional[int] = None


class RatingInDBBase(RatingBase):
    id: int
    user_id: int
    photo_id: int

    model_config = ConfigDict(from_attributes=True)


class RatingResponse(RatingInDBBase):
    pass


class RatingUpdate(BaseModel):
    score: Optional[Decimal] = Field(None, description="The updated rating score between 0 and 6")

    @validator('score', always=True)
    def validate_score(cls, score: Optional[Decimal]) -> Optional[Decimal]:
        if score is not None and not (0 < score < 6):
            raise ValueError('Score must be greater than 0 and less than 6.')
        return score


