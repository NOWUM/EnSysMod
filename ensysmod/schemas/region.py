from typing import Optional

from pydantic import BaseModel


# Shared properties
class RegionBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class RegionCreate(RegionBase):
    name: str
    parent_region: Optional[str] = None


# Properties to receive via API on update
class RegionUpdate(RegionBase):
    name: Optional[str] = None
    parent_Region: Optional[str] = None


class RegionInDBBase(RegionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Region(RegionInDBBase):
    pass


# Additional properties stored in DB
class RegionInDB(RegionInDBBase):
    parent_region: Optional[str] = None
