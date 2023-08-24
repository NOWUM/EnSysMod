from typing import Optional

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import (
    EnergyCommodity,
    EnergyComponent,
    EnergyComponentCreate,
    EnergyComponentUpdate,
)
from ensysmod.utils import validators


class EnergyTransmissionBase(BaseModel):
    """
    Shared attributes for an energy transmission. Used as a base class for all schemas.
    """

    type = EnergyComponentType.TRANSMISSION

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)


class EnergyTransmissionCreate(EnergyTransmissionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy transmission.
    """

    commodity: str = Field(..., description="Commodity of energy transmission.", example="electricity")

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyTransmissionUpdate(EnergyTransmissionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy transmission.
    """

    commodity: Optional[str] = None

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyTransmission(EnergyTransmissionBase):
    """
    Attributes to return via API for an energy transmission.
    """

    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
