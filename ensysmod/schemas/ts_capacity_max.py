from typing import List

from pydantic import BaseModel

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase


class CapacityMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a max capacity. Used as a base class for all schemas.
    """
    max_capacities: List[float]


class CapacityMaxCreate(CapacityMaxBase, RefCRBaseCreate):
    """
    Properties to receive via API on creation of a max capacity.
    """
    pass


class CapacityMaxUpdate(CapacityMaxBase, RefCRBaseUpdate):
    """
    Properties to receive via API on update of a max capacity.
    """
    pass


class CapacityMax(CapacityMaxBase, RefCRBase):
    """
    Properties to return via API for a max capacity.
    """

    class Config:
        orm_mode = True
