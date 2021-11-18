from typing import Optional

from pydantic import BaseModel


# Shared properties
class EnergyConversionBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class EnergyConversionCreate(EnergyConversionBase):
    name: str
    description: Optional[str] = None


# Properties to receive via API on update
class EnergyConversionUpdate(EnergyConversionBase):
    name: Optional[str] = None
    description: Optional[str] = None


class EnergyConversionInDBBase(EnergyConversionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnergyConversion(EnergyConversionInDBBase):
    pass


# Additional properties stored in DB
class EnergyConversionInDB(EnergyConversionInDBBase):
    description: Optional[str] = None
