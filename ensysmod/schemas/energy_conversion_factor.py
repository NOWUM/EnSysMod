from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas import EnergyCommodity


class EnergyConversionFactorBase(BaseModel):
    """
    Shared properties for a energy conversion factor. Used as a base class for all schemas.
    """
    conversion_factor: float


class EnergyConversionFactorCreate(EnergyConversionFactorBase):
    """
    Properties to receive via API on creation of a energy conversion factor.
    """
    ref_dataset: Optional[int] = None
    ref_component: Optional[int] = None
    commodity: str
    pass


class EnergyConversionFactorUpdate(EnergyConversionFactorBase):
    """
    Properties to receive via API on update of a energy conversion factor.
    """
    conversion_factor: Optional[float] = None


class EnergyConversionFactor(EnergyConversionFactorBase):
    """
    Properties to return via API for a energy conversion factor.
    """
    id: int

    commodity: EnergyCommodity

    class Config:
        orm_mode = True
