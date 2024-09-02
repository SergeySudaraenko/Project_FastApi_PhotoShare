from pydantic import BaseModel, ConfigDict

from src.schemas.search import TagBase


class TagCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
