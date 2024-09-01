from fastapi import HTTPException, Depends, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.users import UserUpdateSchema, UserDbModel
from src.database.models import User
from src.repository import user as user_repository
from src.services.auth_service import auth_service

router = APIRouter(prefix="/user", tags=["user"])


def get_current_user():
    pass


@router.get("/me", response_model=UserDbModel)
async def get_my_profile(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.get("/{user_name}", response_model=UserDbModel)
async def get_profile(user_name: str, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_name(user_name, db)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/me/edit", response_model=UserDbModel)
async def edit_my_profile(data: UserUpdateSchema, current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    user = await user_repository.update_user(current_user.username, data, db)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
