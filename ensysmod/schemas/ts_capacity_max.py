from typing import List

from pydantic import BaseModel, validator, Field

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class CapacityMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a max capacity. Used as a base class for all schemas.
    """
    max_capacities: List[float] = Field(..., description="Max capacities for a component in a specific region. "
                                                         "Provide single value or a list of values for each time step "
                                                         "in dataset.",
                                        example=[1.0, 2.0, 3.0])

    # validators
    _valid_max_capacities = validator("max_capacities", allow_reuse=True)(validators.validate_max_capacities)


class CapacityMaxCreate(CapacityMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a max capacity.
    """
    pass


class CapacityMaxUpdate(CapacityMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a max capacity.
    """
    pass


class CapacityMax(CapacityMaxBase, RefCRBase):
    """
    Attributes to return via API for a max capacity.
    """

    class Config:
        orm_mode = True
