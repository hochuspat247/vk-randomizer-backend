from pydantic import BaseModel

class CommunityBase(BaseModel):
    name: str
    description: str | None = None

class CommunityCreate(CommunityBase):
    pass

class Community(CommunityBase):
    id: int

    class Config:
        orm_mode = True
