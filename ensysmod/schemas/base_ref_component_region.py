from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas import EnergyComponent, Region


class RefCRBaseBase(BaseModel):
    """
    Shared properties for a referenced component region model. Used as a base class for all schemas.
    """
    pass


class RefCRBaseCreate(RefCRBaseBase):
    """
    Properties to receive via API on creation of a referenced component region model.
    """
    ref_dataset: int
    component: str
    region: str
    region_to: Optional[int] = None


class RefCRBaseUpdate(RefCRBaseBase):
    """
    Properties to receive via API on update of a referenced component region model.
    """
    pass


class RefCRBase(RefCRBaseBase):
    """
    Properties to return via API for a referenced component region model.
    """
    id: int
    component: EnergyComponent
    region: Region
    region_to: Optional[Region] = None

    class Config:
        orm_mode = True
