from pydantic import Field, field_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactor, EnergyConversionFactorCreate
from ensysmod.utils import validators


class EnergyConversionBase(BaseSchema):
    """
    Shared attributes for an energy conversion. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.CONVERSION

    # validators
    _valid_type = field_validator("type")(validators.validate_energy_component_type)


class EnergyConversionCreate(EnergyConversionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy conversion.
    """

    commodity_unit: str = Field(default=..., description="Commodity the conversion component is based on.", examples=["electricity"])

    conversion_factors: list[EnergyConversionFactorCreate] = Field(
        default=...,
        description="List of conversion factors",
        examples=[
            [
                EnergyConversionFactorCreate(commodity="electricity", conversion_factor=1),
                EnergyConversionFactorCreate(commodity="coal", conversion_factor=-1.6),
            ]
        ],
    )

    # validators
    _valid_conversion_factors = field_validator("conversion_factors")(validators.validate_conversion_factors)
    _valid_commodity_unit = field_validator("commodity_unit")(validators.validate_commodity)


class EnergyConversionUpdate(EnergyConversionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy conversion.
    """

    commodity_unit: str | None = Field(default=None, description="Commodity the conversion component is based on.", examples=["electricity"])

    conversion_factors: list[EnergyConversionFactorCreate] | None = Field(
        default=...,
        description="List of conversion factors",
        examples=[
            [
                EnergyConversionFactorCreate(commodity="electricity", conversion_factor=1),
                EnergyConversionFactorCreate(commodity="coal", conversion_factor=-1.6),
            ]
        ],
    )

    # validators
    _valid_commodity_unit = field_validator("commodity_unit")(validators.validate_unit)


class EnergyConversion(EnergyConversionBase, ReturnSchema):
    """
    Attributes to return via API for an energy conversion.
    """

    component: EnergyComponent = Field(default=..., description="The energy component")
    commodity_unit: EnergyCommodity = Field(default=..., description="Commodity the conversion component is based on.")
    conversion_factors: list[EnergyConversionFactor] = Field(default=..., description="List of conversion factors")
