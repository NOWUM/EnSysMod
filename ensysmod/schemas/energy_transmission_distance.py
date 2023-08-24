from typing import Optional

from pydantic import BaseModel, Field, validator

from ensysmod.schemas.energy_transmission import EnergyTransmission
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class EnergyTransmissionDistanceBase(BaseModel):
    """
    Shared attributes for an energy transmission distance. Used as a base class for all schemas.
    """

    distance: float = Field(..., description="Distance between two regions in unit of dataset.", example=133.4)

    # validators
    _valid_distance = validator("distance", allow_reuse=True)(validators.validate_distance)


class EnergyTransmissionDistanceCreate(EnergyTransmissionDistanceBase):
    """
    Attributes to receive via API on creation of an energy transmission distance.
    """

    ref_dataset: int = Field(None, description="The ID of the referenced dataset.")
    component: str = Field(None, description="The name of the transmission component.")
    region_from: str = Field(None, description="The name of the origin region.")
    region_to: str = Field(None, description="The name of the target region.")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyTransmissionDistanceUpdate(EnergyTransmissionDistanceBase):
    """
    Attributes to receive via API on update of an energy transmission distance.
    """

    distance: Optional[float] = None

    # validators
    _valid_distance = validator("distance", allow_reuse=True)(validators.validate_distance)


class EnergyTransmissionDistance(EnergyTransmissionDistanceBase):
    """
    Attributes to return via API for an energy transmission distance.
    """

    id: int
    transmission: EnergyTransmission
    region_from: Region
    region_to: Region

    class Config:
        orm_mode = True
