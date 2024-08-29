from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import func

from src.routes.profile import get_current_user
from src.database.models import Photo, User, Rating
from src.database.db import get_db
from sqlalchemy.orm import Session as DBSession
from src.schemas.search import PhotoRating

router = APIRouter()

class RatingCreate(BaseModel):
    photo_id: int
    rating: int

class RatingDelete(BaseModel):
    photo_id: int

@router.post("/rate", response_model=PhotoRating)
async def rate_photo(rating: RatingCreate, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if rating.rating < 1 or rating.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
  
    existing_rating = db.query(Rating).filter_by(photo_id=rating.photo_id, user_id=current_user.id).first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="You have already rated this photo")
    
    
    photo = db.query(Photo).filter_by(id=rating.photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.user_id == current_user.id:
        raise HTTPException(status_code=403, detail="You cannot rate your own photo")

    new_rating = Rating(photo_id=rating.photo_id, user_id=current_user.id, rating=rating.rating)
    db.add(new_rating)
    db.commit()
    
    
    average_rating = db.query(func.avg(Rating.rating)).filter_by(photo_id=rating.photo_id).scalar()
    photo.average_rating = average_rating
    db.commit()
    
    return new_rating

@router.delete("/rate", response_model=PhotoRating)
async def delete_rating(rating: RatingDelete, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    rating_to_delete = db.query(Rating).filter_by(photo_id=rating.photo_id, user_id=current_user.id).first()
    if not rating_to_delete:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(rating_to_delete)
    db.commit()
    
    
    average_rating = db.query(func.avg(Rating.rating)).filter_by(photo_id=rating.photo_id).scalar()
    photo = db.query(Photo).filter_by(id=rating.photo_id).first()
    photo.average_rating = average_rating
    db.commit()

    return rating_to_delete

@router.get("/ratings/{photo_id}", response_model=List[PhotoRating])
async def get_ratings(photo_id: int, db: DBSession = Depends(get_db)):
    ratings = db.query(Rating).filter_by(photo_id=photo_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail="No ratings found for this photo")
    return ratings
