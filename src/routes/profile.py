from fastapi import HTTPException, Depends, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
<<<<<<< HEAD
from src.routes.auth import get_refresh_token
from src.schemas.users import UserResponseSchema, UserUpdateSchema
=======
from src.schemas.users import UserUpdateSchema, UserDbModel
>>>>>>> master
from src.database.models import User
from src.repository import user as user_repository
from src.services.auth_service import auth_service

router = APIRouter(prefix="/user", tags=["user"])


def get_current_user():
    pass


<<<<<<< HEAD
@router.get("/me", response_model=UserResponseSchema)
async def get_my_profile(current_user: User = Depends(get_current_user),
                         credentials: HTTPAuthorizationCredentials = Security(get_refresh_token)):
    return User


@router.get("/{username}", response_model=UserResponseSchema)
async def get_profile(username: str):
    user = user_repository.get_user_by_name(username)
=======
@router.get("/me", response_model=UserDbModel)
async def get_my_profile(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.get("/{user_name}", response_model=UserDbModel)
async def get_profile(user_name: str, db: AsyncSession = Depends(get_db)):
    user = await user_repository.get_user_by_name(user_name, db)

>>>>>>> master
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


<<<<<<< HEAD
@router.put("/me/edit", response_model=UserResponseSchema)
async def edit_my_profile(data: UserUpdateSchema, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    user = await user_repository.update_user(current_user.username, data, db)
    return user
=======
@router.put("/me/edit", response_model=UserDbModel)
async def edit_my_profile(data: UserUpdateSchema, current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    user = await user_repository.update_user(current_user.username, data, db)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
>>>>>>> master
