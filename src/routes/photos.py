from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository.photos import create_photo_with_tags

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_photo(
    url: str,
    description: str,
    owner_id: int,
    tag_names: list = [],  # Список тегів, які передаються як параметри
    db: AsyncSession = Depends(get_db)
):
    if len(tag_names) > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can add up to 5 tags only.")
    
    new_photo = await create_photo_with_tags(db, url, description, owner_id, tag_names)
    return {"photo_id": new_photo.id, "message": "Photo created successfully"}
