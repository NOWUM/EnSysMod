from typing import Optional

from pydantic import BaseModel, validator, Field
from pydantic.class_validators import root_validator

from ensysmod.schemas.region import Region
from ensysmod.util import validators


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
    ref_dataset: Optional[int] = Field(None, description="Reference dataset ID. The current dataset will be used.")

    ref_component: Optional[int] = Field(None, description="Reference component ID. "
                                                           "The current component will be used.")
    component: Optional[str] = Field(None, description="Component name. If no ref_component is provided, the name is "
                                                       "used to find the component.")

    ref_region_from: Optional[int] = Field(None, description="Reference region ID.")
    region_from: Optional[str] = Field(None, description="Region name. If no ref_region_from is provided, the name is "
                                                         "used to find the region.")

    ref_region_to: Optional[int] = Field(None, description="Reference region ID.")
    region_to: Optional[str] = Field(None, description="Region name. If no ref_region_to is provided, the name is "
                                                       "used to find the region.")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_optional)

    # _valid_ref_component = root_validator(allow_reuse=True)(validators.validate_component_or_ref)
    _valid_ref_region_from = root_validator(allow_reuse=True)(validators.validate_region_from_or_ref)
    _valid_ref_region_to = root_validator(allow_reuse=True)(validators.validate_region_to_or_ref)


class EnergyTransmissionDistanceUpdate(EnergyTransmissionDistanceBase):
    """
    Attributes to receive via API on update of an energy transmission distance.
    """
    distance: Optional[float] = None


class EnergyTransmissionDistance(EnergyTransmissionDistanceBase):
    """
    Attributes to return via API for an energy transmission distance.
    """
    id: int
    region_from: Region
    region_to: Region

    class Config:
        orm_mode = True
