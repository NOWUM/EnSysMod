from pydantic import Field, field_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, ReturnSchema
from ensysmod.schemas.energy_component import EnergyComponentCreate, EnergyComponentSchema, EnergyComponentUpdate
from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate, EnergyConversionFactorSchema
from ensysmod.utils import validators


class EnergyConversionBase(BaseSchema):
    """
    Shared attributes for an energy conversion. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.CONVERSION


class EnergyConversionCreate(EnergyConversionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy conversion.
    """

    physical_unit: str = Field(
        default=...,
        description="The physical unit the conversion component is based on. It must be one of the commodity units in the dataset.",
        examples=["GW"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
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


class EnergyConversionUpdate(EnergyConversionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy conversion.
    """

    physical_unit: str | None = Field(
        default=None,
        description="The physical unit the conversion component is based on. It must be one of the commodity units in the dataset.",
        examples=["GW"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    conversion_factors: list[EnergyConversionFactorCreate] | None = Field(
        default=None,
        description="List of conversion factors",
        examples=[
            [
                EnergyConversionFactorCreate(commodity="electricity", conversion_factor=1),
                EnergyConversionFactorCreate(commodity="coal", conversion_factor=-1.6),
            ]
        ],
    )


class EnergyConversionSchema(EnergyConversionBase, ReturnSchema):
    """
    Attributes to return via API for an energy conversion.
    """

    component: EnergyComponentSchema
    physical_unit: str
    conversion_factors: list[EnergyConversionFactorSchema]
