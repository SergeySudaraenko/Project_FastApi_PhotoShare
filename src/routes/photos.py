from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import Photo
from routes.comments import get_current_user
from src.database.db import get_db
from src.repository import crud
from src.schemas.photos import PhotoCreate
from typing import List

router = APIRouter()

@router.post("/photos/", response_model=Photo)
async def create_photo(
    photo_create: PhotoCreate,
    tags: List[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await crud.create_photo(db, photo_create, current_user["id"], tags)
