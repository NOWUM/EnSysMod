from typing import Optional, List

from pydantic import BaseModel, validator, Field

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate, EnergyConversionFactor
from ensysmod.util import validators


class EnergyConversionBase(BaseModel):
    """
    Shared attributes for an energy conversion. Used as a base class for all schemas.
    """
    type = EnergyComponentType.CONVERSION

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)


class EnergyConversionCreate(EnergyConversionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy conversion.
    """
    commodity_unit: str = Field(...,
                                description="Commodity the conversion component is based on.",
                                example="electricity")

    conversion_factors: List[EnergyConversionFactorCreate] \
        = Field(...,
                description="List of conversion factors",
                example=[
                    EnergyConversionFactorCreate(commodity="electricity", conversion_factor=1),
                    EnergyConversionFactorCreate(commodity="coal", conversion_factor=-1.6)
                ])

    # validators
    _valid_conversion_factors = validator("conversion_factors", allow_reuse=True)(
        validators.validate_conversion_factors)
    _valid_commodity_unit = validator("commodity_unit", allow_reuse=True)(validators.validate_commodity)


class EnergyConversionUpdate(EnergyConversionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy conversion.
    """
    commodity_unit: Optional[str] = Field(None,
                                          description="Commodity the conversion component is based on.",
                                          example="electricity")

    conversion_factors: Optional[List[EnergyConversionFactorCreate]] \
        = Field(...,
                description="List of conversion factors",
                example=[
                    EnergyConversionFactorCreate(commodity="electricity", conversion_factor=1),
                    EnergyConversionFactorCreate(commodity="coal", conversion_factor=-1.6)
                ])

    # validators
    _valid_commodity_unit = validator("commodity_unit", allow_reuse=True)(validators.validate_unit)


class EnergyConversion(EnergyConversionBase):
    """
    Attributes to return via API for an energy conversion.
    """
    component: EnergyComponent = Field(..., description="The energy component")
    commodity_unit: EnergyCommodity = Field(..., description="Commodity the conversion component is based on.")
    conversion_factors: List[EnergyConversionFactor] = Field(..., description="List of conversion factors")

    class Config:
        orm_mode = True
