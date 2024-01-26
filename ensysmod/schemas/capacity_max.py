from pydantic import Field

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class CapacityMaxBase(RefCRBaseBase):
    """
    Shared attributes for a CapacityMax. Used as a base class for all schemas.
    """

    capacity_max: float = Field(
        default=...,
        description="Maximum capacity for a component in a specific region.",
        examples=[1.0],
        ge=0,
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
