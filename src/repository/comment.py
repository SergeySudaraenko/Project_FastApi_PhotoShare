from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.database.models import Comment

async def create_comment(db: AsyncSession, user_id: int, photo_id: int, comment_text: str):
    new_comment = Comment(user_id=user_id, photo_id=photo_id, comment_text=comment_text)
    db.add(new_comment)
    await db.commit()
    return new_comment

async def get_comment(db: AsyncSession, comment_id: int):
    stmt = select(Comment).filter_by(id=comment_id).options(joinedload(Comment.user), joinedload(Comment.photo))
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_comment(db: AsyncSession, comment_id: int, new_text: str):
    comment = await get_comment(db, comment_id)
    if comment:
        comment.comment_text = new_text
        comment.updated_at = datetime.utcnow()
        await db.commit()
        return comment
    return None

async def delete_comment(db: AsyncSession, comment_id: int):
    comment = await get_comment(db, comment_id)
    if comment:
        await db.delete(comment)
        await db.commit()
        return comment
    return None

async def get_comments_by_photo(db: AsyncSession, photo_id: int):
    stmt = select(Comment).filter_by(photo_id=photo_id).options(joinedload(Comment.user))
    result = await db.execute(stmt)
    return result.scalars().all()
