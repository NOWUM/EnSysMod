from typing import Optional, List

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate, EnergyTransmissionDistance
from ensysmod.util import validators


class EnergyTransmissionBase(BaseModel):
    """
    Shared attributes for an energy transmission. Used as a base class for all schemas.
    """
    type = EnergyComponentType.TRANSMISSION
    loss_per_unit: Optional[float] = Field(None,
                                           description="Loss per length unit of energy transmission.",
                                           example=0.002)

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    _valid_loss_per_unit = validator("loss_per_unit", allow_reuse=True)(validators.validate_loss_per_unit)


class EnergyTransmissionCreate(EnergyTransmissionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy transmission.
    """
    commodity: str = Field(...,
                           description="Commodity of energy transmission.",
                           example="electricity")
    distances: Optional[List[EnergyTransmissionDistanceCreate]] \
        = Field(None,
                description="Distances of energy transmission in the length unit provided with the dataset.")

    # validators
    _valid_distances = validator("distances", allow_reuse=True)(validators.validate_distances)
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)

    class Config:
        schema_extra = {
            "example": {
                "loss_per_unit": 0.002,
                "commodity": "electricity",
                "distances": [
                    {
                        "region_from": "germany",
                        "region_to": "france",
                        "distance": 135.4
                    }
                ]
            }
        }


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
    distances: List[EnergyTransmissionDistance]

    class Config:
        orm_mode = True
