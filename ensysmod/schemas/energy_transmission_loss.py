from pydantic import BaseModel, Field, validator

from ensysmod.schemas.energy_transmission import EnergyTransmission
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class EnergyTransmissionLossBase(BaseModel):
    """
    Shared attributes for an energy transmission loss. Used as a base class for all schemas.
    """

    loss: float = Field(..., description="Relative loss per length unit of energy transmission.", example=0.00003)

    # validators
    _valid_distance = validator("loss", allow_reuse=True)(validators.validate_loss)


class EnergyTransmissionLossCreate(EnergyTransmissionLossBase):
    """
    Attributes to receive via API on creation of an energy transmission loss.
    """

    ref_dataset: int = Field(..., description="The ID of the referenced dataset.")
    component: str = Field(..., description="The name of the transmission component.")
    region: str = Field(..., description="The name of the origin region.")
    region_to: str = Field(..., description="The name of the target region.")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyTransmissionLossUpdate(EnergyTransmissionLossBase):
    """
    Attributes to receive via API on update of an energy transmission loss.
    """
    pass


class EnergyTransmissionLoss(EnergyTransmissionLossBase):
    """
    Attributes to return via API for an energy transmission loss.
    """

    id: int
    transmission: EnergyTransmission
    region: Region
    region_to: Region

    class Config:
        orm_mode = True
