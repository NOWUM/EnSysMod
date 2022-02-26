from typing import Optional

from pydantic import BaseModel, validator, Field

from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.util import validators


class EnergyConversionFactorBase(BaseModel):
    """
    Shared properties for a energy conversion factor. Used as a base class for all schemas.
    """
    conversion_factor: float = Field(..., description="The conversion factor", example=0.9)

    # validators
    _valid_conversion_factor = validator("conversion_factor", allow_reuse=True)(validators.validate_conversion_factor)


class EnergyConversionFactorCreate(EnergyConversionFactorBase):
    """
    Properties to receive via API on creation of a energy conversion factor.
    """
    ref_dataset: Optional[int] = None
    ref_component: Optional[int] = None
    commodity: str = Field(..., description="The commodity", example="electricity")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_optional)
    _valid_ref_component = validator("ref_component", allow_reuse=True)(validators.validate_ref_component_optional)
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


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
