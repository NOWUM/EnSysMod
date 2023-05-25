from typing import List, Optional

from pydantic import BaseModel, Field, validator

from ensysmod.model import EnergyModelOverrideAttribute, EnergyModelOverrideOperation
from ensysmod.schemas import Dataset
from ensysmod.schemas.energy_model_override import (
    EnergyModelOverride,
    EnergyModelOverrideCreate,
    EnergyModelOverrideUpdate,
)
from ensysmod.util import validators


class EnergyModelBase(BaseModel):
    """
    Shared attributes for an energy model. Used as a base class for all schemas.
    """
    name: str = Field(...,
                      description="Name of the energy model.",
                      example="100% CO2 reduction")

    description: Optional[str] = Field(None,
                                       description="Description of the energy model",
                                       example="A model that reduces CO2 emissions by 100%")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyModelCreate(EnergyModelBase):
    """
    Attributes to receive via API on creation of an energy model.
    """
    ref_dataset: int = Field(...,
                             description="ID of the dataset that the energy model is based on.",
                             example=1)

    override_parameters: Optional[List[EnergyModelOverrideCreate]] \
        = Field(None,
                description="Override parameters of the energy model. If given, overrides the values of the referenced dataset.",
                examples=[
                    EnergyModelOverrideCreate(
                        component="CO2 to environment",
                        attribute=EnergyModelOverrideAttribute.yearly_limit,
                        operation=EnergyModelOverrideOperation.set,
                        value=0)
                ])

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyModelUpdate(EnergyModelBase):
    """
    Attributes to receive via API on update of an energy model.
    """
    name: Optional[str] = None
    parameters: Optional[List[EnergyModelOverrideUpdate]] = None


class EnergyModel(EnergyModelBase):
    """
    Attributes to return via API for an energy model.
    """
    id: int
    dataset: Dataset
    parameters: List[EnergyModelOverride]

    class Config:
        orm_mode = True
