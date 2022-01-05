from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.schemas.region import Region
from ensysmod.util import validators


class EnergyTransmissionDistanceBase(BaseModel):
    """
    Shared properties for an energy transmission distance. Used as a base class for all schemas.
    """
    distance: float

    # validators
    _valid_distance = validator("distance", allow_reuse=True)(validators.validate_distance)


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

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_optional)
    _valid_ref_component = validator("ref_component", allow_reuse=True)(validators.validate_ref_component_optional)
    _valid_component = validator("component", allow_reuse=True)(validators.validate_component)
    _valid_ref_region_from = validator("ref_region_from", allow_reuse=True)(validators.validate_ref_region_from)
    _valid_region_from = validator("region_from", allow_reuse=True)(validators.validate_region_from)
    _valid_ref_region_to = validator("ref_region_to", allow_reuse=True)(validators.validate_ref_region_to)
    _valid_region_to = validator("region_to", allow_reuse=True)(validators.validate_region_to)

    # TODO validate that ref_component or component is set
    # TODO validate that ref_region_from or region_from is set
    # TODO validate that ref_region_to or region_to is set


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
