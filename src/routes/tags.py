from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.repository.tag import TagRepository
from src.schemas.tags import PhotoResponse
from src.schemas.tags import TagCreate, TagResponse
from src.services.auth_service import auth_service

router = APIRouter(prefix='/tags', tags=['tag'])


@router.post("/", response_model=TagResponse)
async def create_tag(tag_create: TagCreate, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    return await tag_repo.create_tag(tag_create)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                  current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    tag = await tag_repo.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.get("/name/{tag_name}", response_model=TagResponse)
async def get_tag_by_name(tag_name: str, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    tag = await tag_repo.get_tag_by_name(tag_name)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.get("/", response_model=list[TagResponse])
async def get_tags(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    return await tag_repo.get_tags(skip, limit)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag_name(tag_id: int, new_tag_name: str, db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    updated_tag = await tag_repo.update_tag(tag_id, new_tag_name)
    if not updated_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return updated_tag


@router.get("/count/{photo_id}")
async def get_count_tags_by_photo(photo_id: int, db: AsyncSession = Depends(get_db),
                                  current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    count_tags = await tag_repo.get_count_tags_by_photo(photo_id)
    if count_tags >= 5:
        raise HTTPException(status_code=400, detail="Photo already has 5 tags")
    return count_tags


@router.get("/photos/{tag_id}", response_model=list[PhotoResponse])
async def get_photos_by_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    return await tag_repo.get_photos_by_tag(tag_id)


@router.post("/photos/{photo_id}/tags/", response_model=PhotoResponse)
async def add_tag_to_photo(photo_id: int, new_tag_name: str, db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    tag_repo = TagRepository(db)
    photo = await tag_repo.add_tag(photo_id, new_tag_name)
    if photo:
        return photo
    else:
        return {"message": "Tag not added to photo"}


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete a tag by its ID.

    Args:
        tag_id (int): The ID of the tag to delete.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the tag is not found.
    """
    tag_repo = TagRepository(db)
    await tag_repo.delete_tag(tag_id)
    return None
