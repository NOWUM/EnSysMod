from pydantic import Field, model_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommoditySchema
from ensysmod.schemas.energy_component import EnergyComponentCreate, EnergyComponentSchema, EnergyComponentUpdate
from ensysmod.utils import validators


class EnergySinkBase(BaseSchema):
    """
    Shared attributes for an energy sink. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.SINK

    commodity_cost: float | None = Field(
        default=None,
        description="Cost of the energy sink per unit of energy.",
        examples=[42.2],
        ge=0,
    )
    yearly_limit: float | None = Field(
        default=None,
        description="The yearly limit of the energy sink. If specified, commodity_limit_id must be specified as well.",
        examples=[366.5],
        ge=0,
    )
    commodity_limit_id: str | None = Field(
        default=None,
        description="Commodity limit ID of the energy sink. Required if yearly_limit is specified. The limit is shared among all components of the same commodity_limit_id.",  # noqa: E501
        examples=["CO2"],
        max_length=MAX_STR_LENGTH,
    )

    # validators
    _valid_yearly_limit_and_commodity_limit_id = model_validator(mode="after")(validators.validate_yearly_limit_and_commodity_limit_id)


class EnergySinkCreate(EnergySinkBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy sink.
    """

    commodity_name: str = Field(
        default=...,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergySinkUpdate(EnergySinkBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy sink.
    """

    commodity_name: str | None = Field(
        default=None,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergySinkSchema(EnergySinkBase, ReturnSchema):
    """
    Attributes to return via API for an energy sink.
    """

    component: EnergyComponentSchema
    commodity: EnergyCommoditySchema
