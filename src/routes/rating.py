from typing import List
from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, Role
from src.repository import rating as rating_repository
from src.schemas.rating import RatingInDBBase, AverageRatingResponse
from src.schemas.photos import PhotoResponse
from src.database.db import get_db
from src.services.auth_service import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix='/rating', tags=['ratings'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_post = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_put = RoleAccess([Role.admin, Role.moderator])
allowed_operation_delete = RoleAccess([Role.admin, Role.moderator])


@router.post("/{image_id}/{rating}", response_model=RatingInDBBase, dependencies=[Depends(allowed_operation_post)])
async def create_rate(photo_id: int, rating: int = Path(description="From one to five stars of rating.", ge=1, le=5),
                      db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    new_rate = await rating_repository.create_rating(photo_id, rating, db, current_user)

    if new_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return new_rate


@router.delete("/delete/{rate_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_operation_delete)])
async def delete_rate(rate_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    deleted_rate = await rating_repository.delete_rating(rate_id, db, current_user)

    if deleted_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found or not available.")
    return deleted_rate


@router.get("/image_rating/{photo_id}", response_model=AverageRatingResponse)
async def calculate_rating(photo_id: int, db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):

    average_rate = await rating_repository.calculate_rating(photo_id, db, current_user)

    if average_rate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rating not found or not available.")

    return {"average_rating": average_rate}


@router.get("/images_rating", response_model=List[PhotoResponse])
async def show_images_by_rating(sort_dsc: bool, db: AsyncSession = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    images_by_rating = await rating_repository.show_images_by_rating(sort_dsc, db, current_user)

    if images_by_rating is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Images not found or not available.")

    return images_by_rating
