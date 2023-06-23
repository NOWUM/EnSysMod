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
from ensysmod.util import validators


class EnergySourceBase(BaseModel):
    """
    Shared attributes for an energy source. Used as a base class for all schemas.
    """
    type = EnergyComponentType.SOURCE
    commodity_cost: Optional[float] = Field(None,
                                            description="Cost of the energy source per unit of energy.",
                                            example=42.2)
    yearly_limit: Optional[float] = Field(None,
                                          description="The yearly limit of the energy sink. If specified, commodity_limit_id must be specified as well.",
                                          example=366.5)
    commodity_limit_id: Optional[str] = Field(None,
                                              description="Commodity limit ID of the energy sink. If specified, yearly_limit must be specified as well.",
                                              example="CO2")

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    _valid_commodity_cost = validator("commodity_cost", allow_reuse=True)(validators.validate_commodity_cost)
    _valid_yearly_limit_and_commodity_limit_id = root_validator(allow_reuse=True)(validators.validate_yearly_limit_and_commodity_limit_id)


class EnergySourceCreate(EnergySourceBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy source.
    """
    commodity: str = Field(...,
                           description="Commodity the energy source is associated with.",
                           example="electricity")

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySourceUpdate(EnergySourceBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy source.
    """
    commodity: Optional[str] = None

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySource(EnergySourceBase):
    """
    Attributes to return via API for an energy source.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
