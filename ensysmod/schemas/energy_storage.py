from typing import Optional

from pydantic import BaseModel


# Shared properties
class EnergyStorageBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class EnergyStorageCreate(EnergyStorageBase):
    name: str
    description: Optional[str] = None


# Properties to receive via API on update
class EnergyStorageUpdate(EnergyStorageBase):
    name: Optional[str] = None
    description: Optional[str] = None


class EnergyStorageInDBBase(EnergyStorageBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnergyStorage(EnergyStorageInDBBase):
    pass


# Additional properties stored in DB
class EnergyStorageInDB(EnergyStorageInDBBase):
    description: Optional[str] = None
