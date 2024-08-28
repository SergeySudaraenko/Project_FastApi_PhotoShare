from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.schemas.photos import PhotoCreate
from src.database.models import Comment, Tag, Photo, Role
from src.schemas.comments import CommentCreate, CommentUpdate
from src.schemas.tags import TagCreate
from fastapi import HTTPException

async def create_tag(db: AsyncSession, tag_create: TagCreate) -> Tag:
    db_tag = Tag(tag_name=tag_create.tag_name)
    async with db.begin():
        db.add(db_tag)
        await db.commit()
        await db.refresh(db_tag)
    return db_tag

async def get_tag_by_name(db: AsyncSession, tag_name: str) -> Tag:
    query = select(Tag).filter(Tag.tag_name == tag_name)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_comment(db: AsyncSession, comment_create: CommentCreate, user_id: int, photo_id: int) -> Comment:
    db_comment = Comment(
        comment_text=comment_create.comment_text,
        user_id=user_id,
        photo_id=photo_id
    )
    try:
        async with db.begin():
            db.add(db_comment)
            await db.commit()
            await db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_comment(db: AsyncSession, comment_id: int) -> Comment:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def update_comment(db: AsyncSession, comment_id: int, comment_update: CommentUpdate, user_id: int) -> Comment:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalar_one_or_none()
    if comment:
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        if comment_update.comment_text:
            comment.comment_text = comment_update.comment_text
        comment.updated_at = datetime.utcnow()
        async with db.begin():
            await db.commit()
            await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int, user_id: int, user_role: Role) -> bool:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalar_one_or_none()
    if comment:
        if comment.user_id == user_id or user_role in [Role.admin, Role.moderator]:
            async with db.begin():
                await db.delete(comment)
                await db.commit()
            return True
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    return False

async def get_comments_for_photo(db: AsyncSession, photo_id: int) -> List[Comment]:
    query = select(Comment).filter(Comment.photo_id == photo_id).order_by(Comment.created_at)
    result = await db.execute(query)
    return result.scalars().all()

async def create_photo(db: AsyncSession, photo_create: PhotoCreate, user_id: int, tags: List[str] = None) -> Photo:
  
    if tags and len(tags) > 5:
        raise HTTPException(status_code=400, detail="Cannot add more than 5 tags")
    
 
    db_photo = Photo(
        url=photo_create.url,
        description=photo_create.description,
        owner_id=user_id
    )
    async with db.begin():
        db.add(db_photo)
        await db.commit()
        await db.refresh(db_photo)

    if tags:
      
        existing_tags = set()
        new_tags = []

        for tag_name in tags:
            tag = await get_tag_by_name(db, tag_name)
            if tag:
                existing_tags.add(tag)
            else:
                new_tags.append(tag_name)

        if new_tags:
            
            for tag_name in new_tags:
                tag = await create_tag(db, TagCreate(tag_name=tag_name))
                existing_tags.add(tag)
        
        
        db_photo.photo_tags.extend(existing_tags)
        async with db.begin():
            await db.commit()
            await db.refresh(db_photo)
    
    return db_photo
