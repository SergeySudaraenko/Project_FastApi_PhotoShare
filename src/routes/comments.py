from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User, Role
from src.repository.comment import create_comment, get_comments_by_photo, update_comment, delete_comment
from src.schemas.comments import CommentResponse, CommentDelete
from src.services.auth_service import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/comment", tags=["comment"])
administrator_access = RoleAccess([Role.admin, Role.moderator])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def post_comment(photo_id: int, comment_text: str, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comment = await create_comment(user_id=current_user.id, photo_id=photo_id, text=comment_text, db=db)
    return comment


@router.get("/photo/{photo_id}", response_model=List[CommentResponse])
async def get_comments(photo_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    comments = await get_comments_by_photo(photo_id=photo_id, db=db)
    return comments


@router.put("/{comment_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def edit_comment(comment_id: int, new_text: str, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    updated_comment = await update_comment(comment_id=comment_id, new_text=new_text, user_id=current_user.id, db=db)
    return updated_comment


@router.delete("/{comment_id}", response_model=CommentDelete, dependencies=[Depends(administrator_access)], status_code=status.HTTP_200_OK)
async def delete_comment_route(comment_id: int, db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    del_comment = await delete_comment(db=db, comment_id=comment_id)
    return del_comment
