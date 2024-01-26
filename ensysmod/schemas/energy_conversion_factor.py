from pydantic import Field

from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.energy_commodity import EnergyCommoditySchema


class EnergyConversionFactorBase(BaseSchema):
    """
    Shared attributes for a energy conversion factor. Used as a base class for all schemas.
    """

    conversion_factor: float = Field(
        default=...,
        description="The conversion factor.",
        examples=[0.9],
        ge=-5,
        le=5,
    )


class EnergyConversionFactorCreate(EnergyConversionFactorBase, CreateSchema):
    """
    Attributes to receive via API on creation of a energy conversion factor.
    """

    ref_dataset: int | None = Field(
        default=None,
        description="The reference dataset. The dataset id of the energy conversion component is used.",
        gt=0,
    )
    ref_component: int | None = Field(
        default=None,
        description="The reference component. The component id of the energy conversion component is used.",
        gt=0,
    )
    commodity: str = Field(
        default=...,
        description="Commodity name for this conversion factor.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyConversionFactorUpdate(EnergyConversionFactorBase, UpdateSchema):
    """
    Attributes to receive via API on update of a energy conversion factor.
    """

    conversion_factor: float | None = Field(
        default=None,
        description="The conversion factor.",
        examples=[0.9],
        ge=-5,
        le=5,
    )


class EnergyConversionFactorSchema(EnergyConversionFactorBase, ReturnSchema):
    """
    Attributes to return via API for a energy conversion factor.
    """

    id: int
    commodity: EnergyCommoditySchema
