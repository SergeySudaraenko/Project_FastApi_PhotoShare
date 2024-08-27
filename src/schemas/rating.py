from pydantic import BaseModel, condecimal
from typing import Optional

class RatingBase(BaseModel):
    score: condecimal(gt=0, lt=6) 

class RatingCreate(RatingBase):
    pass

class RatingInDBBase(RatingBase):
    id: int
    user_id: int
    photo_id: int

    class Config:
        orm_mode = True

class Rating(RatingInDBBase):
    pass
