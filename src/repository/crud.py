from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.photos import PhotoCreate
from src.database.models import Comment, Tag, Photo
from src.schemas.comments import CommentCreate, CommentUpdate
from src.schemas.tags import TagCreate


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
   

async def create_comment(db: AsyncSession, comment_create: CommentCreate, user_id: int, photo_id: int) -> Comment:
    db_comment = Comment(
        comment_text=comment_create.comment_text,
        user_id=user_id,
        photo_id=photo_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def update_comment(db: AsyncSession, comment_id: int, comment_update: CommentUpdate) -> Optional[Comment]:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalar_one_or_none()
    if comment:
        comment.comment_text = comment_update.comment_text
        comment.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    query = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(query)
    comment = result.scalar_one_or_none()
    if comment:
        await db.delete(comment)
        await db.commit()
        return True
    return False

async def get_comments_for_photo(db: AsyncSession, photo_id: int) -> List[Comment]:
    query = select(Comment).filter(Comment.photo_id == photo_id).order_by(Comment.created_at)
    result = await db.execute(query)
    return result.scalars().all()

async def create_photo(db: AsyncSession, photo_create: PhotoCreate, user_id: int, tags: Optional[List[str]] = None) -> Photo:
    db_photo = Photo(
        url=photo_create.url,
        description=photo_create.description,
        owner_id=user_id
    )
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)

    if tags:
        for tag_name in tags:
            tag = await get_tag_by_name(db, tag_name)
            if not tag:
                tag = await create_tag(db, TagCreate(tag_name=tag_name))
            db_photo.photo_tags.append(tag)
        await db.commit()
        await db.refresh(db_photo)

    return db_photo

