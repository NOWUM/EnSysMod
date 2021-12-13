from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas import Dataset


class EnergyModelBase(BaseModel):
    """
    Shared properties for an energy model. Used as a base class for all schemas.
    """
    name: str
    yearly_co2_limit: Optional[float] = None
    description: Optional[str] = None


class EnergyModelCreate(EnergyModelBase):
    """
    Properties to receive via API on creation of an energy model.
    """
    ref_dataset: int


class EnergyModelUpdate(EnergyModelBase):
    """
    Properties to receive via API on update of an energy model.
    """
    name: Optional[str] = None


class EnergyModel(EnergyModelBase):
    """
    Properties to return via API for an energy model.
    """
    id: int
    dataset: Dataset

    class Config:
        orm_mode = True
