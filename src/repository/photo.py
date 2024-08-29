from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.database.models import Photo, Tag
from src.repository.crud import get_or_create

async def create_photo_with_tags(db: AsyncSession, url: str, description: str, owner_id: int, tag_names: list):
    # Створення нового фото
    new_photo = Photo(url=url, description=description, owner_id=owner_id)
    db.add(new_photo)
    
    # Перевірка і додавання тегів
    tags = []
    for tag_name in tag_names:
        tag = await get_or_create(db, Tag, tag_name=tag_name)
        tags.append(tag)
    
    # Додавання тегів до фото
    new_photo.photo_tags = tags
    await db.commit()
    return new_photo

async def get_or_create(db: AsyncSession, model, **kwargs):
    async with db.begin():
        stmt = select(model).filter_by(**kwargs)
        result = await db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            instance = model(**kwargs)
            db.add(instance)
            await db.commit()
        return instance
