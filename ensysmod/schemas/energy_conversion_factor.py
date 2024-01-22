from pydantic import Field, field_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.utils import validators


class EnergyConversionFactorBase(BaseSchema):
    """
    Shared attributes for a energy conversion factor. Used as a base class for all schemas.
    """

    conversion_factor: float = Field(default=..., description="The conversion factor.", examples=[0.9])

    # validators
    _valid_conversion_factor = field_validator("conversion_factor")(validators.validate_conversion_factor)


class EnergyConversionFactorCreate(EnergyConversionFactorBase, CreateSchema):
    """
    Attributes to receive via API on creation of a energy conversion factor.
    """

    ref_dataset: int | None = Field(default=None, description="The reference dataset. The dataset id of the energy conversion component is used.")
    ref_component: int | None = Field(
        default=None, description="The reference component. The component id of the energy conversion component is used."
    )
    commodity: str = Field(default=..., description="Commodity name for this conversion factor.", examples=["electricity"])

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_optional)
    _valid_ref_component = field_validator("ref_component")(validators.validate_ref_component_optional)
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergyConversionFactorUpdate(EnergyConversionFactorBase, UpdateSchema):
    """
    Attributes to receive via API on update of a energy conversion factor.
    """

    conversion_factor: float | None = None


class EnergyConversionFactor(EnergyConversionFactorBase, ReturnSchema):
    """
    Attributes to return via API for a energy conversion factor.
    """

    id: int
    commodity: EnergyCommodity
