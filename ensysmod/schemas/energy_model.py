from typing import Optional, List

from pydantic import BaseModel, validator, Field

from ensysmod.schemas import Dataset
from ensysmod.schemas.energy_model_parameter import EnergyModelParameter, EnergyModelParameterCreate, \
    EnergyModelParameterUpdate
from ensysmod.util import validators
from ensysmod.model import EnergyModelParameterAttribute, EnergyModelParameterOperation


class EnergyModelBase(BaseModel):
    """
    Shared properties for an energy model. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the energy model", example="100% CO2 reduction")
    description: Optional[str] = Field(None, description="Description of the energy model",
                                       example="A model that reduces CO2 emissions by 100%")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyModelCreate(EnergyModelBase):
    """
    Properties to receive via API on creation of an energy model.
    """
    ref_dataset: int
    parameters: Optional[List[EnergyModelParameterCreate]] = Field(None, description="Parameters of the energy model",
                                                                   examples=[
                                                                       EnergyModelParameterCreate(
                                                                           component="CO2 to environment",
                                                                           attribute=EnergyModelParameterAttribute.yearly_limit,
                                                                           operation=EnergyModelParameterOperation.set,
                                                                           value=0)
                                                                   ])

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyModelUpdate(EnergyModelBase):
    """
    Properties to receive via API on update of an energy model.
    """
    name: Optional[str] = None
    parameters: Optional[List[EnergyModelParameterUpdate]] = None


class EnergyModel(EnergyModelBase):
    """
    Properties to return via API for an energy model.
    """
    id: int
    dataset: Dataset
    parameters: List[EnergyModelParameter]

    class Config:
        orm_mode = True
