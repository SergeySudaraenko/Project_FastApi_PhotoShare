from pydantic import BaseModel, condecimal


class RatingBase(BaseModel):
    score: condecimal(gt=0, lt=6)  # type: ignore

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
