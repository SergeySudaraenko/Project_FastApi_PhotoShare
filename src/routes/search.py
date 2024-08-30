from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from src.database.models import Photo, Tag

from src.database.db import get_db
from sqlalchemy.orm import Session as DBSession

router = APIRouter(prefix="/search", tags=["search"])


class SearchParams(BaseModel):
    keyword: Optional[str] = None
    tag: Optional[str] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@router.get("/search", response_model=List[Photo])
async def search_photos(params: SearchParams, db: DBSession = Depends(get_db)):
    query = db.query(Photo)

    if params.keyword:
        query = query.filter(Photo.description.ilike(f"%{params.keyword}%"))

    if params.tag:
        tag = db.query(Tag).filter_by(name=params.tag).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        query = query.filter(Photo.tags.any(Tag.id == tag.id))

    if params.min_rating:
        query = query.filter(Photo.average_rating >= params.min_rating)

    if params.max_rating:
        query = query.filter(Photo.average_rating <= params.max_rating)

    if params.start_date:
        query = query.filter(Photo.created_at >= params.start_date)

    if params.end_date:
        query = query.filter(Photo.created_at <= params.end_date)

    results = query.all()
    if not results:
        raise HTTPException(
            status_code=404, detail="No photos found matching the criteria"
        )

    return results
