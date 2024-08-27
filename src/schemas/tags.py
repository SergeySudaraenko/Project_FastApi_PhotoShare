from pydantic import BaseModel


class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    pass


class TagInDBBase(TagBase):
    id: int

    class Config:
        orm_mode = True


class Tag(TagInDBBase):
    pass
