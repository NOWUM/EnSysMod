from typing import Optional

from pydantic import BaseModel


# Shared properties
class CapacityBase(BaseModel):
    year: Optional[str] = None
    quantity: Optional[str] = None


# Properties to receive via API on creation
class CapacityCreate(CapacityBase):
    year: int
    quantity: int
    region: str
    source: str


# Properties to receive via API on update
class CapacityUpdate(CapacityBase):
    year: Optional[int] = None
    quantity: Optional[int] = None
    region: Optional[str] = None
    source: Optional[str] = None


class CapacityInDBBase(CapacityBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Capacity(CapacityInDBBase):
    pass


# Additional properties stored in DB
class CapacityInDB(CapacityInDBBase):
    region: Optional[int] = None
    source: Optional[int] = None
