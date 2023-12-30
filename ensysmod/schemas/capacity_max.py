from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class CapacityMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a CapacityMax. Used as a base class for all schemas.
    """

    capacity_max: NonNegativeFloat = Field(
        ...,
        description="Maximum capacity for a component in a specific region.",
        example=1.0,
    )


class CapacityMaxCreate(CapacityMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a CapacityMax.
    """


class CapacityMaxUpdate(CapacityMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a CapacityMax.
    """


class CapacityMax(CapacityMaxBase, RefCRBase):
    """
    Attributes to return via API for a CapacityMax.
    """

    class Config:
        orm_mode = True
