from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.database.models import Role
from src.repository.comment import (
    create_comment,
    update_comment,
    delete_comment,
    get_comment,
    get_comments_by_photo,
)
from src.services.auth_service import auth_service

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_comment(
    photo_id: int,
    comment_text: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(lambda token: auth_service.get_current_user(token)),
):
    new_comment = await create_comment(db, current_user["id"], photo_id, comment_text)
    return {"comment_id": new_comment.id, "message": "Comment created successfully"}


@router.put("/{comment_id}", status_code=status.HTTP_200_OK)
async def edit_comment(
    comment_id: int,
    new_text: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(lambda token: auth_service.get_current_user(token)),
):
    comment = await get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    if comment.user_id != current_user["id"] and current_user["role"] not in [
        Role.admin,
        Role.moderator,
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this comment",
        )
    updated_comment = await update_comment(db, comment_id, new_text)
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return {"message": "Comment updated successfully"}


@router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(lambda token: auth_service.get_current_user(token)),
):
    comment = await get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    if comment.user_id != current_user["id"] and current_user["role"] not in [
        Role.admin,
        Role.moderator,
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )
    deleted_comment = await delete_comment(db, comment_id)
    if not deleted_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return {"message": "Comment deleted successfully"}


@router.get("/photo/{photo_id}", response_model=list)
async def get_comments(photo_id: int, db: AsyncSession = Depends(get_db)):
    comments = await get_comments_by_photo(db, photo_id)
    return comments
