from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Photo
from src.schemas.photos import PhotoCreate


async def create_photo(db: AsyncSession, photo: PhotoCreate) -> Photo:
    new_photo = Photo(url=photo.url, description=photo.description, owner_id=photo.owner_id)
    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)
    return new_photo


async def get_photo_by_id(photo_id: int, db: AsyncSession):
    result = await db.execute(select(Photo).filter(Photo.id == int(photo_id)))
    photo = result.scalar_one_or_none()
    return photo


async def get_photo_by_url(photo_url: int, db: AsyncSession):
    result = await db.execute(select(Photo).filter(Photo.url == photo_url))
    photo = result.scalar_one_or_none()
    return photo


async def create(photo_url: str, photo, db: AsyncSession):
    image = Photo(url=photo_url, owner_id=photo.owner_id, description=f'{photo.description} - transformed')
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image
