from typing import Optional, List

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.schemas.energy_transmission_distance import EnergyTransmissionDistanceCreate, EnergyTransmissionDistance


class EnergyTransmissionBase(BaseModel):
    """
    Shared properties for an energy transmission. Used as a base class for all schemas.
    """
    commodity: str
    type = EnergyComponentType.TRANSMISSION
    loss_per_unit: Optional[float] = None


class EnergyTransmissionCreate(EnergyTransmissionBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy transmission.
    """
    distances: Optional[List[EnergyTransmissionDistanceCreate]] = None


class EnergyTransmissionUpdate(EnergyTransmissionBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy transmission.
    """
    commodity: Optional[str] = None


class EnergyTransmission(EnergyTransmissionBase):
    """
    Properties to return via API for an energy transmission.
    """
    component: EnergyComponent
    commodity: EnergyCommodity
    distances: List[EnergyTransmissionDistance]

    class Config:
        orm_mode = True
