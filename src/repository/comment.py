from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.database.models import Comment
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


async def create_comment(db: AsyncSession, user_id: int, photo_id: int, comment_text: str):
    new_comment = Comment(user_id=user_id, photo_id=photo_id, comment_text=comment_text)
    try:
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)  
        return new_comment
    except SQLAlchemyError as e:
        await db.rollback()  

        raise HTTPException(status_code=500, detail="An error occurred while creating the comment")


async def get_comment(db: AsyncSession, comment_id: int):
    try:
        stmt = select(Comment).filter(Comment.id == comment_id, Comment.is_deleted == False).options(
            joinedload(Comment.user), 
            joinedload(Comment.photo)
        )
        print("Executing statement:", stmt)
        result = await db.execute(stmt)
        comment = result.scalars().first()
        return comment
    except Exception as e:
        print(f"Error fetching comment: {e}")
    
        raise

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
        comment.is_deleted = True
        comment.updated_at = datetime.utcnow()
        await db.commit()
        return comment
    return None

async def get_comments_by_photo(db: AsyncSession, photo_id: int):
    stmt = select(Comment).filter_by(photo_id=photo_id, is_deleted=False).options(joinedload(Comment.user))
    result = await db.execute(stmt)
    return result.scalars().all()

