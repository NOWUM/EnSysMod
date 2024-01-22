from pydantic import Field, field_validator, model_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
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
    )
    yearly_limit: float | None = Field(
        default=None,
        description="The yearly limit of the energy sink. If specified, commodity_limit_id must be specified as well.",
        examples=[366.5],
    )
    commodity_limit_id: str | None = Field(
        default=None,
        description="Commodity limit ID of the energy sink. Required if yearly_limit is specified. The limit is shared among all components of the same commodity_limit_id.",  # noqa: E501
        examples=["CO2"],
    )

    # validators
    _valid_type = field_validator("type")(validators.validate_energy_component_type)
    _valid_commodity_cost = field_validator("commodity_cost")(validators.validate_commodity_cost)
    _valid_yearly_limit_and_commodity_limit_id = model_validator(mode="after")(validators.validate_yearly_limit_and_commodity_limit_id)


class EnergySinkCreate(EnergySinkBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy sink.
    """

    commodity: str = Field(default=..., description="Commodity the energy sink is based on.", examples=["electricity"])

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergySinkUpdate(EnergySinkBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy sink.
    """

    commodity: str | None = None

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergySink(EnergySinkBase, ReturnSchema):
    """
    Attributes to return via API for an energy sink.
    """

    component: EnergyComponent
    commodity: EnergyCommodity
