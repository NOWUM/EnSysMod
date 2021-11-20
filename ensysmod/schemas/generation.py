from typing import Optional

from pydantic import BaseModel


# Shared properties
class GenerationBase(BaseModel):
    year: Optional[int] = None
    quantity: Optional[int] = None


# Properties to receive via API on creation
class GenerationCreate(GenerationBase):
    year: int
    quantity: int
    region: str
    source: str


# Properties to receive via API on update
class GenerationUpdate(GenerationBase):
    year: Optional[int] = None
    quantity: Optional[int] = None
    region: Optional[str] = None
    source: Optional[str] = None


class GenerationInDBBase(GenerationBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Generation(GenerationInDBBase):
    pass


# Additional properties stored in DB
class GenerationInDB(GenerationInDBBase):
    region: str
    source: str
