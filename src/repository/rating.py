from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.models import Rating, Photo
from src.schemas.rating import RatingCreate, RatingUpdate


def create_rating(db: Session, rating: RatingCreate, photo_id: int, user_id: int):
    existing_rating = db.query(Rating).filter_by(photo_id=photo_id, user_id=user_id).first()
    if existing_rating:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this photo.")
    # Перевіряємо, що фото існує
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found.")

    db_rating = Rating(photo_id=photo_id, user_id=user_id, **rating.dict())
    try:
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error saving rating.")

    return db_rating


def get_ratings_for_photo(db: Session, photo_id: int):
    return db.query(Rating).filter_by(photo_id=photo_id).all()


def update_rating(db: Session, rating_id: int, rating_update: RatingUpdate):
    db_rating = db.query(Rating).filter_by(id=rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found.")
    for key, value in rating_update.dict(exclude_unset=True).items():
        setattr(db_rating, key, value)
    db.commit()
    db.refresh(db_rating)
    return db_rating


def delete_rating(db: Session, rating_id: int):
    db_rating = db.query(Rating).filter_by(id=rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found.")
    db.delete(db_rating)
    db.commit()
    return {"detail": "Rating deleted successfully."}
