from pydantic import Field

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate
from ensysmod.schemas.region import RegionSchema


class TransmissionLossBase(RefCRBaseBase):
    """
    Shared attributes for an TransmissionLoss. Used as a base class for all schemas.
    """

    loss: float = Field(
        default=...,
        description="Relative loss per length unit of energy transmission.",
        examples=[0.00003],
        ge=0,
        le=1,
    )


class TransmissionLossCreate(TransmissionLossBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of an TransmissionLoss.
    """

    region_to: str = Field(
        default=...,
        description="The name of the target region.",
        examples=["france"],
    )


class TransmissionLossUpdate(TransmissionLossBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of an TransmissionLoss.
    """


class TransmissionLossSchema(TransmissionLossBase, RefCRBase):
    """
    Attributes to return via API for an TransmissionLoss.
    """

    region_to: RegionSchema
