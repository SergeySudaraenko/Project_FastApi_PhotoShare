from fastapi import HTTPException, status
from sqlalchemy import and_, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Rating, Photo
from src.schemas.photos import PhotoResponseRating


async def create_rating(photo_id: int, rating: int, db: AsyncSession, user):
    is_self_image_result = await db.execute(select(Photo).filter(and_(Photo.id == photo_id, Photo.owner_id == user.id)))
    is_self_image = is_self_image_result.scalar_one_or_none()

    already_rated_result = await db.execute(
        select(Rating).filter(and_(Rating.photo_id == photo_id, Rating.user_id == user.id)))
    already_rated = already_rated_result.scalar_one_or_none()

    image_exists_result = await db.execute(select(Photo).filter(Photo.id == photo_id))
    image_exists = image_exists_result.scalar_one_or_none()

    if is_self_image:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate own image.")
    if already_rated:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="It`s not possible to rate twice.")
    if image_exists:
        new_rate = Rating(photo_id=photo_id, value=rating, user_id=user.id)
        db.add(new_rate)
        await db.commit()
        await db.refresh(new_rate)

        return new_rate


async def calculate_rating(photo_id: int, db: AsyncSession):
    result = await db.execute(select(func.avg(Rating.value)).filter(Rating.photo_id == photo_id))
    average_rating = result.scalar()

    print('average_rating', average_rating)
    return average_rating


async def show_images_by_rating(sort_dsc: bool, db: AsyncSession):
    average_rating_label = "calculated_average_rating"

    sort_order = desc(average_rating_label) if sort_dsc else asc(average_rating_label)

    stmt = (select(Photo, func.avg(Rating.value).label(average_rating_label)).join(Photo.ratings).group_by(
        Photo.id).order_by(sort_order).having(func.avg(Rating.value).isnot(None)))

    result = await db.execute(stmt)
    images_with_ratings = result.all()

    response = [
        PhotoResponseRating(id=photo.id, url=photo.url, description=photo.description, created_at=photo.created_at,
                            updated_at=photo.updated_at, owner_id=photo.owner_id, rating=average_rating) for
        photo, average_rating in images_with_ratings]

    return response


async def delete_rating(rating_id: int, db: AsyncSession, user):
    result = await db.execute(select(Rating).filter(and_(Rating.id == rating_id, Photo.owner_id == user.id)))
    rate = result.scalars().first()

    if rate:
        await db.delete(rate)
        await db.commit()
        return {"detail": "Rating deleted successfully."}

    return {"detail": "Rating not found."}
