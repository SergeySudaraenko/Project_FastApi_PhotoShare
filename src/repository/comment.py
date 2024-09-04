from datetime import datetime, timezone
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.database.models import Comment, Photo


async def create_comment(user_id: int, photo_id: int, text: str, db: AsyncSession) -> Comment:
    # Перевіряємо існування фото
    stmt = select(Photo).filter(Photo.id == photo_id)
    result = await db.execute(stmt)
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    # Додаємо коментар
    new_comment = Comment(user_id=user_id, photo_id=photo_id, comment_text=text)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def get_comments_by_photo(photo_id: int, db: AsyncSession) -> List[Comment]:
    # Перевіряємо існування фото
    stmt = select(Photo).filter(Photo.id == photo_id)
    result = await db.execute(stmt)
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    # Зчитуємо коментарі
    stmt = select(Comment).filter(Comment.photo_id == photo_id, Comment.is_deleted == False).options(joinedload(Comment.user))
    result = await db.execute(stmt)
    comments = result.scalars().all()
    return comments


async def update_comment(comment_id: int, new_text: str, user_id: int, db: AsyncSession) -> Optional[Comment]:
    # Перевіряємо існування коментаря
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    # Перевіряємо права користувача
    if comment.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if comment.is_deleted == True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Comment is deleted")
    # Змінюємо текст коментаря
    comment.comment_text = new_text
    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: int):
    # Перевіряємо існування коментаря
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comment.is_deleted = True
    await db.commit()
    await db.refresh(comment)
    return comment
