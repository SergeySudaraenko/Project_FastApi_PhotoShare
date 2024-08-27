from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.user import UserResponseSchema, UserUpdateSchema
from src.database.models import User
from src.repository import user as user_repository


router = APIRouter(prefix="/user", tags=["user"])

def get_current_user():
    pass


@router.get("/me", response_model=UserResponseSchema)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    return user

@router.get("/{username}", response_model=UserResponseSchema)
async def get_profile(username: str):
    user = user_repository.get_user_by_name(username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")



@router.put("/me/edit", response_model=UserResponseSchema)
async def edit_my_profile(data: UserUpdateSchema, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await user_repository.update_user(current_user.username, data, db)
    return user


