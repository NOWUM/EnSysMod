from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity


class EnergyConversionBase(BaseModel):
    """
    Shared properties for an energy conversion. Used as a base class for all schemas.
    """
    commodity_unit: str
    type = EnergyComponentType.CONVERSION


class EnergyConversionCreate(EnergyConversionBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy conversion.
    """
    pass


class EnergyConversionUpdate(EnergyConversionBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy conversion.
    """
    commodity_unit: Optional[str] = None


class EnergyConversion(EnergyConversionBase):
    """
    Properties to return via API for an energy conversion.
    """
    component: EnergyComponent
    commodity_unit: EnergyCommodity

    class Config:
        orm_mode = True
