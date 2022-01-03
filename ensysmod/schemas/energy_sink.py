from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate, EnergyComponent, EnergyCommodity
from ensysmod.util import validators


class EnergySinkBase(BaseModel):
    """
    Shared properties for an energy sink. Used as a base class for all schemas.
    """
    type = EnergyComponentType.SINK

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)


class EnergySinkCreate(EnergySinkBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy sink.
    """
    commodity: str
    
    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySinkUpdate(EnergySinkBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy sink.
    """
    commodity: Optional[str] = None
    
    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergySink(EnergySinkBase):
    """
    Properties to return via API for an energy sink.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
