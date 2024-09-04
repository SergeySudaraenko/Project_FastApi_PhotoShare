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

    model_config = ConfigDict(from_attributes=True)


class PhotoBase(BaseModel):
    pass


class PhotoResponse(PhotoBase):
    uid: str
    url: str
