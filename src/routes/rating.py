from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.config import User
from routes.comments import get_current_user
from src.database.db import get_db
from src.database.models import Rating, Photo
from src.schemas.rating import RatingCreate


router = APIRouter()

@router.post("/rate/", response_model=RatingCreate)
def rate_photo(rating: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    photo = db.query(Photo).filter(Photo.id == rating.photo_id).first()
    if photo.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot rate your own photo.")
    
    
    existing_rating = db.query(Rating).filter(Rating.user_id == current_user.id, Rating.photo_id == rating.photo_id).first()
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this photo.")
    
    new_rating = Rating(score=rating.score, user_id=current_user.id, photo_id=rating.photo_id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    
    return new_rating

@router.get("/photos/{photo_id}/average_rating", response_model=float)
def get_average_rating(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    
    return photo.average_rating

@router.delete("/rate/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found")
    
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    db.delete(rating)
    db.commit()
    
    return {"detail": "Rating deleted"}
