from pydantic import Field

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class CapacityFixBase(RefCRBaseBase):
    """
    Shared attributes for a CapacityFix. Used as a base class for all schemas.
    """

    capacity_fix: float = Field(
        default=...,
        description="Fixed capacity for a component in a specific region.",
        examples=[1.0],
        ge=0,
    )


class CapacityFixCreate(CapacityFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a CapacityFix.
    """


class CapacityFixUpdate(CapacityFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a CapacityFix.
    """


class CapacityFix(CapacityFixBase, RefCRBase):
    """
    Attributes to return via API for a CapacityFix.
    """
