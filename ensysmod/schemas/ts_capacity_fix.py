from typing import List

from pydantic import BaseModel, validator, Field

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class CapacityFixBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a fix capacity. Used as a base class for all schemas.
    """
    fix_capacities: List[float] = Field(...,
                                        description="Fix capacities for a component in a specific region. "
                                                    "Provide single value or a list of values for each time step "
                                                    "in dataset.",
                                        example=[4.0, 5.0, 6.0])

    # validators
    _valid_fix_capacities = validator("fix_capacities", allow_reuse=True)(validators.validate_fix_capacities)


class CapacityFixCreate(CapacityFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a fix capacity.
    """
    pass


class CapacityFixUpdate(CapacityFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a fix capacity.
    """
    pass


class CapacityFix(CapacityFixBase, RefCRBase):
    """
    Attributes to return via API for a fix capacity.
    """

    class Config:
        orm_mode = True
