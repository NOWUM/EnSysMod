from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class CapacityFixBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a fix capacity. Used as a base class for all schemas.
    """

    fix_capacity: NonNegativeFloat = Field(
        ...,
        description="Fixed capacity for a component in a specific region.",
        example=1.0,
    )


class CapacityFixCreate(CapacityFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a fix capacity.
    """


class CapacityFixUpdate(CapacityFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a fix capacity.
    """


class CapacityFix(CapacityFixBase, RefCRBase):
    """
    Attributes to return via API for a fix capacity.
    """

    class Config:
        orm_mode = True
