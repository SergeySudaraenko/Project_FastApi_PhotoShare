from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import Photo, Tag, User
from src.schemas.photos import PhotoResponse
from src.services.auth_service import auth_service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/search", response_model=List[PhotoResponse])
async def search_photos(keyword: Optional[str] = None, tag: Optional[str] = None, min_rating: Optional[float] = None,
                        max_rating: Optional[float] = None, start_date: Optional[str] = None,
                        end_date: Optional[str] = None, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    query = select(Photo)

    if keyword:
        query = query.where(Photo.description.ilike(f"%{keyword}%"))

    if tag:
        tag_obj = await db.execute(select(Tag).filter_by(name=tag))
        tag_obj = tag_obj.scalar()
        if not tag_obj:
            raise HTTPException(status_code=404, detail="Tag not found")
        query = query.where(Photo.photo_tags.any(Tag.id == tag_obj.id))

    if min_rating:
        query = query.where(Photo.average_rating >= min_rating)

    if max_rating:
        query = query.where(Photo.average_rating <= max_rating)

    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.where(Photo.created_at >= start_date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.where(Photo.created_at <= start_date_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    results = await db.execute(query)
    photos = results.scalars().all()
    if not photos:
        raise HTTPException(status_code=404, detail="No photos found matching the criteria")
    return photos
