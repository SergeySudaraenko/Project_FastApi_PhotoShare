from pydantic import BaseModel, ConfigDict

from src.schemas.search import TagBase


class TagCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagUpdate(TagBase):
    pass


class TagResponse(TagBase):


    id: int
    name: str

    class Config:
        orm_mode = True

class PhotoBase(BaseModel):
    pass

class PhotoResponse(PhotoBase):
    id: int
    url: str

