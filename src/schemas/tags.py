from pydantic import BaseModel



# Pydantic Models
class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagResponse(TagBase):
    id: int

    class Config:
        orm_mode = True

class PhotoBase(BaseModel):
    pass

class PhotoResponse(PhotoBase):
    id: int
    url: str









# class PhotoTagBase(BaseModel):
#     photo_id: int
#     tag_id: int
#
#
# class PhotoTagCreate(PhotoTagBase):
#     pass
#
#
# class PhotoTagInDBBase(PhotoTagBase):
#     class Config:
#         orm_mode = True
#
#
# class PhotoTagResponse(PhotoTagInDBBase):
#     pass
