from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from src.database.db import get_db
from src.database.models import Photo, User
from src.repository import photo as photo_repository
from src.schemas.photos import PhotoCreate, PhotoResponse, PhotoTransformModel
from src.services import cloudinary_service
from src.services import qr_code_service
from src.services.auth_service import auth_service

router = APIRouter(prefix="/photo", tags=["photo"])


@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo(
        photo_id: int,
        db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
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
        db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
):
    async with db as session:

        result = await session.execute(select(Photo).filter(Photo.id == photo_id))
        photo = result.scalar_one_or_none()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if photo.owner_id != current_user.id and current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Not enough permissions")

        photo.description = description

        await session.commit()
        await session.refresh(photo)

    return photo


@router.delete("/{photo_id}")
async def delete_photo(photo_id: int, db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    async with db as session:
        result = await session.execute(select(Photo).filter(Photo.id == photo_id))
        photo = result.scalar_one_or_none()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if photo.owner_id != current_user.id and not current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Not enough permissions")

        await session.delete(photo)
        await session.commit()

    return {"detail": "Photo deleted"}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_photo(
        file: UploadFile = File(...),
        description: str = None,
        db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)
):
    if file.content_type.split('/')[0] != 'image':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid file type. Only images are allowed.")

    try:
        image_url = await cloudinary_service.upload_image(file.file)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    photo_data = PhotoCreate(
        url=image_url,
        description=description,
        owner_id=current_user.id
    )

    new_photo = await photo_repository.create_photo(db=db, photo=photo_data)
    return new_photo


@router.post("/transform", status_code=status.HTTP_201_CREATED)
async def create_transformed_image(body: PhotoTransformModel,
                                   current_user: User = Depends(auth_service.get_current_user),
                                   db: AsyncSession = Depends(get_db)):
    """
    For transformation use:
        - "grayscale"
        - "cartoonify"
        - "radius"
        - "standard"
        - "vectorize"
    """
    photo = await photo_repository.get_photo_by_id(body.id, db)

    if not photo.url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    transformed_photo_url = await cloudinary_service.get_transformed_photo(photo.url, body.transformation)

    image_in_db = await photo_repository.get_photo_by_url(transformed_photo_url, db)

    if photo.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")

    if image_in_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resource already exists")

    new_image = await photo_repository.create(transformed_photo_url, photo, db)

    return new_image


@router.post("/qrcode/{photo_id}", status_code=status.HTTP_201_CREATED)
async def generate_qrcode(image_id: int,
                          current_user: User = Depends(auth_service.get_current_user),
                          db: AsyncSession = Depends(get_db)):
    photo = await photo_repository.get_photo_by_id(image_id, db)

    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    qr_code = await qr_code_service.create_qr_code(photo.url)

    if qr_code is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return StreamingResponse(qr_code, media_type="image/png", status_code=status.HTTP_201_CREATED)
