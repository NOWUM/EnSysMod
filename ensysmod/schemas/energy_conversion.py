from typing import Optional, List

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate, EnergyConversionFactor


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
    conversion_factors: List[EnergyConversionFactorCreate]


class EnergyConversionUpdate(EnergyConversionBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy conversion.
    """
    commodity_unit: Optional[str] = None
    conversion_factors: Optional[List[EnergyConversionFactorCreate]] = None  # update = delete and recreate


class EnergyConversion(EnergyConversionBase):
    """
    Properties to return via API for an energy conversion.
    """
    component: EnergyComponent
    commodity_unit: EnergyCommodity
    conversion_factors: List[EnergyConversionFactor]

    class Config:
        orm_mode = True
