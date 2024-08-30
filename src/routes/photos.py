from fastapi import APIRouter, Depends, HTTPException, status,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository.photo import create_photo_with_tags

router = APIRouter(prefix="/photo", tags=["photo"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_photo(
    file: UploadFile,
    description: str,
    owner_id: int,
    # tag_names: list = [],
    # db: AsyncSession = Depends(get_db),
):
    # if len(tag_names) > 5:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="You can add up to 5 tags only.",
    #     )

    # new_photo = await create_photo_with_tags(db, url, description, owner_id, tag_names)
    # return {"photo_id": new_photo.id, "message": "Photo created successfully"}
    pass   
# 
    """
    1)Додати схему вілідації-Клас в схемах
    2)Збережений файл треба заливати на клаудінарі і посиланя з клаудінарі зберігати в бд.
    3)Теги переробити.
    """