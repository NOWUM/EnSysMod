from typing import Optional

from pydantic import BaseModel, validator, Field

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.util import validators


class EnergySourceBase(BaseModel):
    """
    Shared attributes for an energy source. Used as a base class for all schemas.
    """
    type = EnergyComponentType.SOURCE
    commodity_cost: Optional[float] = Field(None,
                                            description="Cost of the energy source per unit of energy.",
                                            example=42.2)

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    _valid_commodity_cost = validator("commodity_cost", allow_reuse=True)(validators.validate_commodity_cost)


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
