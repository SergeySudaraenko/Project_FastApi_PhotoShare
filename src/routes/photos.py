from fastapi import APIRouter, Depends, HTTPException, status,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.routes.profile import get_current_user
from src.database.db import get_db
from src.repository.photo import create_photo_with_tags
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas.photos import PhotoCreate
from src.repository.photo import create_photo
from sqlalchemy import select

from src.database.models import Photo, User


router = APIRouter(prefix="/photo", tags=["photo"])



@router.get("/{photo_id}")
async def get_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Photo).filter(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    return photo


@router.put("/{photo_id}")
async def update_photo_description(
    photo_id: int,
    description: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # if not current_user:
    #     raise HTTPException(status_code=401, detail="Not authenticated")

    async with db as session:
        
        result = await session.execute(select(Photo).filter(Photo.id == photo_id))
        photo = result.scalar_one_or_none()
        
        
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        
        if photo.owner_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        
        photo.description = description
        
        
        await session.commit()
        await session.refresh(photo)  
        
    return photo



@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    async with db as session:
        result = await session.execute(select(Photo).filter(Photo.id == photo_id))
        photo = result.scalar_one_or_none()
        
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        # if current_user is None:
        #     raise HTTPException(status_code=401, detail="Not authenticated")

        if photo.owner_id != current_user.id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        
        await session.delete(photo)
        await session.commit()
    
    return {"detail": "Photo deleted"}


   

@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    description: str = None,
    db: AsyncSession = Depends(get_db),  
    current_user: User = Depends(get_current_user)
):

    # Створення нової світлини
    photo = PhotoCreate(url=url, description=description, owner_id=current_user.id)
    return create_photo(db=db, photo=photo)
# 
    """
    1)Додати схему вілідації-Клас в схемах
    2)Збережений файл треба заливати на клаудінарі і посиланя з клаудінарі зберігати в бд.
    3)Теги переробити.
    """