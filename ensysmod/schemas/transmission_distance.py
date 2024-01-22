from pydantic import Field, field_validator

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class TransmissionDistanceBase(RefCRBaseBase):
    """
    Shared attributes for an TransmissionDistance. Used as a base class for all schemas.
    """

    distance: float = Field(default=..., description="Distance between two regions in unit of dataset.", examples=[133.4])

    # validators
    _valid_distance = field_validator("distance")(validators.validate_distance)


class TransmissionDistanceCreate(TransmissionDistanceBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of an TransmissionDistance.
    """

    region_to: str = Field(default=..., description="The name of the target region.", examples=["france"])


class TransmissionDistanceUpdate(TransmissionDistanceBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of an TransmissionDistance.
    """


class TransmissionDistance(TransmissionDistanceBase, RefCRBase):
    """
    Attributes to return via API for an TransmissionDistance.
    """

    region_to: Region
