from pydantic import BaseModel, Field, validator

from ensysmod.schemas.dataset import Dataset
from ensysmod.schemas.energy_component import EnergyComponent
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class RefCRBaseBase(BaseModel):
    """
    Shared attributes for a referenced component region model. Used as a base class for all schemas.
    """


class RefCRBaseCreate(RefCRBaseBase):
    """
    Attributes to receive via API on creation of a referenced component region model.
    """

    ref_dataset: int = Field(..., description="The ID of the referenced dataset. Current dataset is used as default.")
    component: str = Field(..., description="The name of the component.", example="heat_pump")
    region: str = Field(..., description="The name of the region.", example="germany")
    region_to: str | None = Field(None, description="Optional region to name, if needed.", example="france")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class RefCRBaseUpdate(RefCRBaseBase):
    """
    Attributes to receive via API on update of a referenced component region model.
    """


class RefCRBase(RefCRBaseBase):
    """
    Attributes to return via API for a referenced component region model.
    """

    id: int
    dataset: Dataset
    component: EnergyComponent
    region: Region
    region_to: Region | None = None

    class Config:
        orm_mode = True
