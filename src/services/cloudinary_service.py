import re

import cloudinary
from cloudinary.uploader import upload
from fastapi import HTTPException
from starlette import status

from src.config.config import settings
from src.config.transformations import Transformation

# Налаштування Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


async def upload_image(file):
    try:
        result = upload(file, folder="your_folder_name")  # Ви можете вказати папку за потреби
        url = result.get("secure_url")
        return url
    except Exception as e:
        raise e


async def get_transformed_photo(photo_url: str, transformation: str):
    public_id = re.search(r'/upload/(.+?)(?:\.\w+)?$', photo_url).group(1)

    if transformation in Transformation.name.keys():
        print(Transformation.name.get(transformation))
        transformed_photo_url, _ = cloudinary.utils.cloudinary_url(public_id,transformation=[Transformation.name.get(transformation)])
        return transformed_photo_url

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transformation Not Found")
