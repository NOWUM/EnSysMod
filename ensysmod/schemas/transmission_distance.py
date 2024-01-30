from pydantic import Field

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH
from ensysmod.schemas.region import RegionSchema


class TransmissionDistanceBase(RefCRBaseBase):
    """
    Shared attributes for an TransmissionDistance. Used as a base class for all schemas.
    """

    distance: float = Field(
        default=...,
        description="Distance between two regions in unit of dataset.",
        examples=[133.4],
        ge=0,
    )


class TransmissionDistanceCreate(TransmissionDistanceBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of an TransmissionDistance.
    """

    region_to_name: str = Field(
        default=...,
        description="The name of the target region.",
        examples=["france"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class TransmissionDistanceUpdate(TransmissionDistanceBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of an TransmissionDistance.
    """


class TransmissionDistanceSchema(TransmissionDistanceBase, RefCRBase):
    """
    Attributes to return via API for an TransmissionDistance.
    """

    region_to: RegionSchema
