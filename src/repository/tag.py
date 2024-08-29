from sqlalchemy.orm import Session
from src.database.models import Photo, Tag
from src.schemas.tags import PhotoTag, TagCreate
from fastapi import HTTPException, status

def create_tag(db: Session, tag: TagCreate):
   
    db_tag = db.query(Tag).filter_by(name=tag.name).first()
    if db_tag:
        return db_tag
    
    
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    
    return db_tag

def get_tags(db: Session):
    return db.query(Tag).all()

def associate_tag_with_photo(db: Session, photo_id: int, tag_name: str):
    
    photo = db.query(Photo).filter_by(id=photo_id).first()
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found."
        )
    
    
    tag = db.query(Tag).filter_by(name=tag_name).first()
    if not tag:
        tag = create_tag(db, TagCreate(name=tag_name))
    
    
    db_photo_tag = PhotoTag(photo_id=photo_id, tag_id=tag.id)
    db.add(db_photo_tag)
    db.commit()
    
    return {"detail": "Tag associated with photo successfully."}

def get_tags_for_photo(db: Session, photo_id: int):
    
    return db.query(Tag).join(PhotoTag).filter(PhotoTag.photo_id == photo_id).all()
