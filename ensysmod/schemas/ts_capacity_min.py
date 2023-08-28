from typing import List

from pydantic import BaseModel, Field, validator

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)
from ensysmod.utils import validators


class CapacityMinBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a min capacity. Used as a base class for all schemas.
    """
    min_capacities: List[float] = Field(..., description="Min capacities for a component in a specific region. "
                                                         "Provide single value or a list of values for each time step "
                                                         "in dataset.",
                                        example=[1.0, 2.0, 3.0])

    # validators
    _valid_min_capacities = validator("min_capacities", allow_reuse=True)(validators.validate_min_capacities)


class CapacityMinCreate(CapacityMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a min capacity.
    """
    pass


class CapacityMinUpdate(CapacityMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a min capacity.
    """
    pass


class CapacityMin(CapacityMinBase, RefCRBase):
    """
    Attributes to return via API for a min capacity.
    """

    class Config:
        orm_mode = True
