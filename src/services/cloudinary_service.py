import cloudinary
from cloudinary.uploader import upload
from src.config.config import settings

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
