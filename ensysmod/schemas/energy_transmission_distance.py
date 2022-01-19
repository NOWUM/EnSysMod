from typing import Optional

from pydantic import BaseModel, validator
from pydantic.class_validators import root_validator

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

    _valid_ref_component = root_validator(allow_reuse=True)(validators.validate_component_or_ref)
    _valid_ref_region_from = root_validator(allow_reuse=True)(validators.validate_region_from_or_ref)
    _valid_ref_region_to = root_validator(allow_reuse=True)(validators.validate_region_to_or_ref)



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
