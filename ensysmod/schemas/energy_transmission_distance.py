from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas.region import Region


class EnergyTransmissionDistanceBase(BaseModel):
    """
    Shared properties for an energy transmission distance. Used as a base class for all schemas.
    """
    distance: float


class EnergyTransmissionDistanceCreate(EnergyTransmissionDistanceBase):
    """
    Properties to receive via API on creation of an energy transmission distance.
    """
    ref_dataset: Optional[int] = None

    ref_component: Optional[int] = None
    component: Optional[str] = None

    ref_region_from: Optional[int] = None
    region_from: Optional[str] = None

    ref_region_to: Optional[int] = None
    region_to: Optional[str] = None


class EnergyTransmissionDistanceUpdate(EnergyTransmissionDistanceBase):
    """
    Properties to receive via API on update of an energy transmission distance.
    """
    distance: Optional[float] = None


class EnergyTransmissionDistance(EnergyTransmissionDistanceBase):
    """
    Properties to return via API for an energy transmission distance.
    """
    id: int
    region_from: Region
    region_to: Region

    class Config:
        orm_mode = True
