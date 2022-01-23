from typing import Optional, List

from pydantic import BaseModel

from ensysmod.schemas import Dataset
from ensysmod.schemas.energy_model_parameter import EnergyModelParameter, EnergyModelParameterCreate, \
    EnergyModelParameterUpdate


class EnergyModelBase(BaseModel):
    """
    Shared properties for an energy model. Used as a base class for all schemas.
    """
    name: str
    description: Optional[str] = None


class EnergyModelCreate(EnergyModelBase):
    """
    Properties to receive via API on creation of an energy model.
    """
    ref_dataset: int
    parameters: Optional[List[EnergyModelParameterCreate]] = None


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
