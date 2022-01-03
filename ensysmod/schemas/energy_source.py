from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.util import validators


class EnergySourceBase(BaseModel):
    """
    Shared properties for an energy source. Used as a base class for all schemas.
    """
    type = EnergyComponentType.SOURCE
    commodity_cost: Optional[float] = None

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    _valid_commodity_cost = validator("commodity_cost", allow_reuse=True)(validators.validate_commodity_cost)


class EnergySourceCreate(EnergySourceBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy source.
    """
    commodity: str

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySourceUpdate(EnergySourceBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy source.
    """
    commodity: Optional[str] = None

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySource(EnergySourceBase):
    """
    Properties to return via API for an energy source.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
