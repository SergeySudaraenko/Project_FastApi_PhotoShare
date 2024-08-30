from sqlalchemy.orm import Session
from src.database.models import Photo, Tag
from src.schemas.tags import TagCreate
from fastapi import HTTPException, status

def create_tag(db: Session, tag: TagCreate):
    db_tag = db.query(Tag).filter_by(tag_name=tag.name).first()
    if db_tag:
        return db_tag

    db_tag = Tag(tag_name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag

def get_tags(db: Session):
    return db.query(Tag).all()

def associate_tag_with_photo(db: Session, photo_id: int, tag_name: str):
    # Знайти фото за ID
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found."
        )

    # Знайти тег за ім'ям або створити його
    tag = db.query(Tag).filter_by(tag_name=tag_name).first()
    if not tag:
        tag = create_tag(db, TagCreate(name=tag_name))

    # Додати тег до фото через relationship
    if tag not in photo.photo_tags:
        photo.photo_tags.append(tag)  # Використовуємо relationship для асоціації
        db.commit()

    return {"detail": "Tag associated with photo successfully."}

def get_tags_for_photo(db: Session, photo_id: int):
    # Повернути теги для вказаного фото через асоціативну таблицю
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found."
        )
    return photo.photo_tags  # Отримуємо пов'язані теги напряму
