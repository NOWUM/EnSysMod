from typing import Optional

from pydantic import BaseModel


# Shared properties
class EnergySourceBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class EnergySourceCreate(EnergySourceBase):
    name: str
    description: Optional[str] = None


# Properties to receive via API on update
class EnergySourceUpdate(EnergySourceBase):
    name: Optional[str] = None
    description: Optional[str] = None


class EnergySourceInDBBase(EnergySourceBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnergySource(EnergySourceInDBBase):
    pass


# Additional properties stored in DB
class EnergySourceInDB(EnergySourceInDBBase):
    description: Optional[str] = None
