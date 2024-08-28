from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repositories_users
from src.services.auth import auth_service
from src.config.config import settings
from src.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'ContactsApp/{user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'ContactsApp/{user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repositories_users.update_avatar(user.email, src_url, db)
    return user