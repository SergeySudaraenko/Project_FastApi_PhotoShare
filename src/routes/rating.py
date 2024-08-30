from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func, select
from src.routes.profile import get_current_user
from src.database.models import Photo, User, Rating
from src.database.db import get_db
from src.schemas.search import PhotoRating
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rating", tags=["rating"])

class RatingCreate(BaseModel):
    photo_id: int
    rating: int

class RatingDelete(BaseModel):
    photo_id: int

@router.post("/rate", response_model=PhotoRating)
async def rate_photo(
    rating: RatingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(current_user)
    
    if rating.rating < 1 or rating.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    stmt = select(Rating).filter_by(photo_id=rating.photo_id, user_id=current_user.id)
    result = await db.execute(stmt)
    existing_rating = result.scalar_one_or_none()
    
    if existing_rating:
        raise HTTPException(status_code=400, detail="You have already rated this photo")
    stmt = select(Photo).filter_by(id=rating.photo_id)
    result = await db.execute(stmt)
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.owner_id == current_user.id:
        raise HTTPException(status_code=403, detail="You cannot rate your own photo")

    new_rating = Rating(
        photo_id=rating.photo_id, user_id=current_user.id, value=rating.rating
    )
    db.add(new_rating)
    db.commit()
    stmt = select(func.avg(Rating.value)).filter_by(photo_id=rating.photo_id)
    result = await db.execute(stmt)
    average_rating = result.scalar_one_or_none()
    photo.average_rating = average_rating if average_rating is not None else 0
    db.commit()

    return new_rating

@router.delete("/rate", response_model=PhotoRating)
async def delete_rating(
    rating: RatingDelete,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rating_to_delete = (
        db.query(Rating)
        .filter_by(photo_id=rating.photo_id, user_id=current_user.id)
        .first()
    )
    if not rating_to_delete:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating_to_delete)
    db.commit()

    average_rating = (
        db.query(func.avg(Rating.value)).filter_by(photo_id=rating.photo_id).scalar()
    )
    photo = db.query(Photo).filter_by(id=rating.photo_id).first()
    if photo:
        photo.average_rating = average_rating if average_rating is not None else 0
        db.commit()

    return rating_to_delete

@router.get("/ratings/{photo_id}", response_model=List[PhotoRating])
async def get_ratings(photo_id: int, db: DBSession = Depends(get_db)):
    ratings = db.query(Rating).filter_by(photo_id=photo_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail="No ratings found for this photo")
    return ratings
