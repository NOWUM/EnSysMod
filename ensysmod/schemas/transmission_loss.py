from pydantic import BaseModel, Field, validator

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class TransmissionLossBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for an TransmissionLoss. Used as a base class for all schemas.
    """

    loss: float = Field(..., description="Relative loss per length unit of energy transmission.", example=0.00003)

    # validators
    _valid_distance = validator("loss", allow_reuse=True)(validators.validate_loss)


class TransmissionLossCreate(TransmissionLossBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of an TransmissionLoss.
    """

    region_to: str = Field(..., description="The name of the target region.", example="france")


class TransmissionLossUpdate(TransmissionLossBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of an TransmissionLoss.
    """


class TransmissionLoss(TransmissionLossBase, RefCRBase):
    """
    Attributes to return via API for an TransmissionLoss.
    """

    region_to: Region

    class Config:
        orm_mode = True
