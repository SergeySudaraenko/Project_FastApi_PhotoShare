# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.database.db import get_db
# from src.repository import crud
# from src.schemas.comments import CommentCreate, CommentUpdate
# from src.database.models import Comment
# from src.database.models import Role
# from fastapi.security import OAuth2PasswordBearer
# from typing import List
#
# router = APIRouter()
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     # Тут треба функція для перевірки токена користувача(чи не писати зовсім)
#     pass
#
#
# @router.post("/comments/", response_model=Comment)
# async def create_comment(
#         comment: CommentCreate,
#         photo_id: int,
#         db: AsyncSession = Depends(get_db),
#         current_user: dict = Depends(get_current_user)
# ):
#     user_id = current_user["id"]
#     return await crud.create_comment(db, comment, user_id, photo_id)
#
#
# @router.get("/comments/{comment_id}", response_model=Comment)
# async def read_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
#     comment = await crud.get_comment(db, comment_id)
#     if comment is None:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     return comment
#
#
# @router.put("/comments/{comment_id}", response_model=Comment)
# async def update_comment(
#         comment_id: int,
#         comment: CommentUpdate,
#         db: AsyncSession = Depends(get_db),
#         current_user: dict = Depends(get_current_user)
# ):
#     existing_comment = await crud.get_comment(db, comment_id)
#     if existing_comment is None:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     if existing_comment.user_id != current_user["id"] and current_user["role"] not in [Role.admin, Role.moderator]:
#         raise HTTPException(status_code=403, detail="Not authorized to update this comment")
#     return await crud.update_comment(db, comment_id, comment)
#
#
# @router.delete("/comments/{comment_id}", response_model=dict)
# async def delete_comment(
#         comment_id: int,
#         db: AsyncSession = Depends(get_db),
#         current_user: dict = Depends(get_current_user)
# ):
#     existing_comment = await crud.get_comment(db, comment_id)
#     if existing_comment is None:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     if existing_comment.user_id != current_user["id"] and current_user["role"] not in [Role.admin, Role.moderator]:
#         raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
#     success = await crud.delete_comment(db, comment_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Comment not found")
#     return {"status": "Comment deleted"}
#
#
# @router.get("/photos/{photo_id}/comments", response_model=List[Comment])
# async def read_comments_for_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
#     return await crud.get_comments_for_photo(db, photo_id)
