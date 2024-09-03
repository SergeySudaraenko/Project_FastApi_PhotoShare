from fastapi import HTTPException, status
from src.database.models import Photo, Tag, photo_tag
from src.schemas.tags import TagCreate
from sqlalchemy import select,  func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exists



class TagRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tag_by_name(self, tag_name: str) -> Tag:
        query = select(Tag).where(Tag.name == tag_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_tag(self, tag_create: TagCreate) -> Tag:
        tag= await self.get_tag_by_name(tag_create.name)
        if tag:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")
        new_tag = Tag(
            **tag_create.model_dump())
          
        self.session.add(new_tag)
        await self.session.commit()
        await self.session.refresh(new_tag)
        return new_tag

    async def get_tag(self, tag_id: int) -> Tag:
        query = select(Tag).where(Tag.id == tag_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()



    async def get_tags(self,skip: int = 0, limit: int = 10) -> list[Tag]:
        query = select(Tag).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()


    async def get_photos_by_tag(self, tag_id: int, skip: int = 0, limit: int = 10) -> list[Photo]:
        query = select(Photo).join(photo_tag).join(Tag).filter(Tag.id == tag_id).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()



    async def update_tag(self, tag_id: int, new_tag_name: str) -> Tag:
        tag = await self.get_tag(tag_id)

        if tag:

            tag.name=new_tag_name
            await self.session.commit()
            await self.session.refresh(tag)
        return tag



    async def get_photo_by_id(self, photo_id: int) -> Photo:
        query = select(Photo).where(Photo.id == photo_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def get_count_tags_by_photo(self, photo_id)-> int:
        tag_count_query = select(func.count()).select_from(photo_tag).filter(photo_tag.c.photo_id == photo_id)
        tag_count = await self.session.execute(tag_count_query)
        tag_count = tag_count.scalar()
        return tag_count

    async def tag_exists_for_photo(self, photo_id: int, tag_name: str) -> bool:
        query = select(exists().where(photo_tag.c.photo_id == photo_id).where(photo_tag.c.tag_id == Tag.id).where(
            Tag.name == tag_name))
        result = await self.session.execute(query)
        return result.scalar()

    async def add_tag(self, photo_id: int, new_tag_name: str) -> Photo | None:
        new_tag_name = new_tag_name.strip()
        if not new_tag_name:
            raise HTTPException(status_code=400, detail="Tag name is required")

        tag_exists = await self.tag_exists_for_photo(photo_id, new_tag_name)
        if tag_exists:
            raise HTTPException(status_code=400, detail="Tag already exists for this photo")

        photo = await self.get_photo_by_id(photo_id)
        if not photo:
            raise HTTPException(status_code=400, detail="Tag photo not found")

        count_tags=await self.get_count_tags_by_photo(photo_id)
        if count_tags >= 5:
            raise HTTPException(status_code=400, detail="Photo already has 5 tags")


        tag= await self.get_tag_by_name(new_tag_name)
        if not tag:
            tag = Tag(name=new_tag_name)
            self.session.add(tag)
            await self.session.flush()


        # Принудительно загружаем связанные теги
        await self.session.refresh(photo, ['photo_tags'])
        photo.photo_tags.append(tag)
        await self.session.commit()
        await self.session.refresh(photo)
        return photo


    async def delete_tag(self, tag_id: int) -> None:
        tag = await self.get_tag(tag_id)
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
        await self.session.delete(tag)
        await self.session.commit()


