from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.schemas import Dataset
from ensysmod.util import validators


class RegionBase(BaseModel):
    """
    Shared properties for a region. Used as a base class for all schemas.
    """
    name: str

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)


class RegionCreate(RegionBase):
    """
    Properties to receive via API on creation of a region.
    """
    ref_dataset: int

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class RegionUpdate(RegionBase):
    """
    Properties to receive via API on update of a region.
    """
    name: Optional[str] = None


class Region(RegionBase):
    """
    Properties to return via API for a region.
    """
    id: int
    dataset: Dataset

    class Config:
        orm_mode = True
