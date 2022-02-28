from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.schemas.energy_component import EnergyComponent
from ensysmod.schemas.region import Region


class RefCRBaseBase(BaseModel):
    """
    Shared attributes for a referenced component region model. Used as a base class for all schemas.
    """
    pass


class RefCRBaseCreate(RefCRBaseBase):
    """
    Attributes to receive via API on creation of a referenced component region model.
    """
    ref_dataset: int = Field(..., description="The ID of the referenced dataset. Current dataset is used as default.")
    component: str = Field(..., description="The name of the component.", example="heat_pump")
    region: str = Field(..., description="The name of the region.", example="germany")
    region_to: Optional[str] = Field(None, description="Optional region to name, if needed.", example="france")


class RefCRBaseUpdate(RefCRBaseBase):
    """
    Attributes to receive via API on update of a referenced component region model.
    """
    pass


class RefCRBase(RefCRBaseBase):
    """
    Attributes to return via API for a referenced component region model.
    """
    id: int
    component: EnergyComponent
    region: Region
    region_to: Optional[Region] = None

    class Config:
        orm_mode = True
