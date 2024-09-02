from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Tag, Photo
from src.schemas.tags import TagCreate
from fastapi import HTTPException, status

async def create_tag(db: AsyncSession, tag_create: TagCreate) -> Tag:
    db_tag = Tag(tag_name=tag_create.tag_name)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def get_tag_by_name(db: AsyncSession, tag_name: str) -> Optional[Tag]:
    query = select(Tag).filter(Tag.tag_name == tag_name)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_tags(db: AsyncSession) -> List[Tag]:
    query = select(Tag)
    result = await db.execute(query)
    return result.scalars().all()

async def associate_tag_with_photo(db: AsyncSession, photo_id: int, tag_name: str) -> dict:
    # Знайти фото за ID
    photo_query = select(Photo).filter(Photo.id == photo_id)
    photo_result = await db.execute(photo_query)
    photo = photo_result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фото не знайдено."
        )

    # Знайти тег за ім'ям або створити його
    tag = await get_tag_by_name(db, tag_name)
    if not tag:
        tag_create = TagCreate(tag_name=tag_name)
        tag = await create_tag(db, tag_create)

    # Додати тег до фото через relationship
    if tag not in photo.photo_tags:
        photo.photo_tags.append(tag)  # Використовуємо relationship для асоціації
        await db.commit()

    return {"detail": "Тег успішно асоційований з фото."}

async def get_tags_for_photo(db: AsyncSession, photo_id: int) -> List[Tag]:
    # Повернути теги для вказаного фото через асоціативну таблицю
    photo_query = select(Photo).filter(Photo.id == photo_id)
    photo_result = await db.execute(photo_query)
    photo = photo_result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фото не знайдено."
        )
    return photo.photo_tags  # Отримуємо пов'язані теги напряму
