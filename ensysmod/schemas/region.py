from typing import Optional

from pydantic import BaseModel, validator, Field

from ensysmod.schemas import Dataset
from ensysmod.util import validators


class RegionBase(BaseModel):
    """
    Shared attributes for a region. Used as a base class for all schemas.
    """
    name: str = Field(...,
                      description="Unique name of the region.",
                      example="germany")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)


class RegionCreate(RegionBase):
    """
    Attributes to receive via API on creation of a region.
    """
    ref_dataset: int = Field(..., description="ID of the dataset to use as reference.", example=1)

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class RegionUpdate(RegionBase):
    """
    Attributes to receive via API on update of a region.
    """
    name: Optional[str] = Field(None, description="New name of the region", example="germany")


class Region(RegionBase):
    """
    Attributes to return via API for a region.
    """
    id: int
    dataset: Dataset

    class Config:
        orm_mode = True
