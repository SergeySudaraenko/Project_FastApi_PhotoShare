from datetime import datetime, timezone
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from src.database.models import Comment
from src.schemas.search import CommentUpdate


async def create_comment(db: AsyncSession, user_id: int, photo_id: int, text: str) -> Comment:
    new_comment = Comment(
        user_id=user_id,
        photo_id=photo_id,
        comment_text=text
    )
    try:
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Сталася помилка під час створення коментаря") from e


async def get_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    try:
        stmt = select(Comment).filter(Comment.id == comment_id, Comment.is_deleted.is_(False)).options(
            joinedload(Comment.user), joinedload(Comment.photo))
        result = await db.execute(stmt)
        comment = result.scalars().first()
        return comment
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Сталася помилка під час отримання коментаря") from e


async def update_comment(db: AsyncSession, comment_id: int, new_text: str) -> Optional[Comment]:
    comment = await get_comment(db, comment_id)
    if comment:
        comment.comment_text = new_text
        comment.updated_at = datetime.now(timezone.utc)
        try:
            await db.commit()
            await db.refresh(comment)
            return comment
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Сталася помилка під час оновлення коментаря") from e
    return None


async def delete_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    comment = await get_comment(db, comment_id)
    if comment:
        comment.is_deleted = True
        comment.updated_at = datetime.now(timezone.utc)
        try:
            await db.commit()
            await db.refresh(comment)
            return comment
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Сталася помилка під час видалення коментаря") from e
    return None


async def get_comments_by_photo(db: AsyncSession, photo_id: int) -> List[Comment]:
    stmt = select(Comment).filter_by(photo_id=photo_id, is_deleted=False).options(joinedload(Comment.user))
    result = await db.execute(stmt)
    return list(result.scalars().all())
