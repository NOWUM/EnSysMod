from pydantic import Field, field_validator, model_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
from ensysmod.utils import validators


class EnergySourceBase(BaseSchema):
    """
    Shared attributes for an energy source. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.SOURCE

    commodity_cost: float | None = Field(
        default=None,
        description="Cost of the energy source per unit of energy.",
        examples=[42.2],
    )
    yearly_limit: float | None = Field(
        default=None,
        description="The yearly limit of the energy sink. If specified, commodity_limit_id must be specified as well.",
        examples=[366.5],
    )
    commodity_limit_id: str | None = Field(
        default=None,
        description="Commodity limit ID of the energy sink. If specified, yearly_limit must be specified as well.",
        examples=["CO2"],
    )

    # validators
    _valid_type = field_validator("type")(validators.validate_energy_component_type)
    _valid_commodity_cost = field_validator("commodity_cost")(validators.validate_commodity_cost)
    _valid_yearly_limit_and_commodity_limit_id = model_validator(mode="after")(validators.validate_yearly_limit_and_commodity_limit_id)


class EnergySourceCreate(EnergySourceBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy source.
    """

    commodity: str = Field(default=..., description="Commodity the energy source is associated with.", examples=["electricity"])

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergySourceUpdate(EnergySourceBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy source.
    """

    commodity: str | None = None

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergySource(EnergySourceBase, ReturnSchema):
    """
    Attributes to return via API for an energy source.
    """

    component: EnergyComponent
    commodity: EnergyCommodity
