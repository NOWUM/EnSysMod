from typing import Optional

from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import (
    EnergyCommodity,
    EnergyComponent,
    EnergyComponentCreate,
    EnergyComponentUpdate,
)
from ensysmod.utils import validators


class EnergySinkBase(BaseModel):
    """
    Shared attributes for an energy sink. Used as a base class for all schemas.
    """
    type = EnergyComponentType.SINK
    commodity_cost: Optional[float] = Field(
        None,
        description="Cost of the energy sink per unit of energy.",
        example=42.2,
    )
    yearly_limit: Optional[float] = Field(
        None,
        description="The yearly limit of the energy sink. If specified, commodity_limit_id must be specified as well.",
        example=366.5,
    )
    commodity_limit_id: Optional[str] = Field(
        None,
        description="Commodity limit ID of the energy sink. Required if yearly_limit is specified. The limit is shared among all components of the same commodity_limit_id.",  # noqa: E501
        example="CO2",
    )

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    _valid_commodity_cost = validator("commodity_cost", allow_reuse=True)(validators.validate_commodity_cost)
    _valid_yearly_limit_and_commodity_limit_id = root_validator(allow_reuse=True)(validators.validate_yearly_limit_and_commodity_limit_id)


class EnergySinkCreate(EnergySinkBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy sink.
    """
    commodity: str = Field(...,
                           description="Commodity the energy sink is based on.",
                           example="electricity")

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySinkUpdate(EnergySinkBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy sink.
    """
    commodity: Optional[str] = None

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySink(EnergySinkBase):
    """
    Attributes to return via API for an energy sink.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
