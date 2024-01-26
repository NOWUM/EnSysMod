from pydantic import Field

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class CapacityMinBase(RefCRBaseBase):
    """
    Shared attributes for a CapacityMin. Used as a base class for all schemas.
    """

    capacity_min: float = Field(
        default=...,
        description="Minimum capacity for a component in a specific region.",
        examples=[1.0],
        ge=0,
    )


class CapacityMinCreate(CapacityMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a CapacityMin.
    """


class CapacityMinUpdate(CapacityMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a CapacityMin.
    """


class CapacityMin(CapacityMinBase, RefCRBase):
    """
    Attributes to return via API for a CapacityMin.
    """
