from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class CapacityMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a max capacity. Used as a base class for all schemas.
    """

    max_capacity: NonNegativeFloat = Field(
        ...,
        description="Maximum capacity for a component in a specific region.",
        example=1.0,
    )


class CapacityMaxCreate(CapacityMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a max capacity.
    """


class CapacityMaxUpdate(CapacityMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a max capacity.
    """


class CapacityMax(CapacityMaxBase, RefCRBase):
    """
    Attributes to return via API for a max capacity.
    """

    class Config:
        orm_mode = True
