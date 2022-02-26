from typing import List

from pydantic import BaseModel, validator

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class CapacityFixBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a max capacity. Used as a base class for all schemas.
    """
    fix_capacities: List[float]

    # validators
    _valid_fix_capacities = validator("fix_capacities", allow_reuse=True)(validators.validate_fix_capacities)


class CapacityFixCreate(CapacityFixBase, RefCRBaseCreate):
    """
    Properties to receive via API on creation of a max capacity.
    """
    pass


class CapacityFixUpdate(CapacityFixBase, RefCRBaseUpdate):
    """
    Properties to receive via API on update of a max capacity.
    """
    pass


class CapacityFix(CapacityFixBase, RefCRBase):
    """
    Properties to return via API for a max capacity.
    """

    class Config:
        orm_mode = True
