from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity


class EnergyStorageBase(BaseModel):
    """
    Shared properties for an energy storage. Used as a base class for all schemas.
    """
    commodity: str
    type = EnergyComponentType.STORAGE

    charge_efficiency: Optional[float] = None
    discharge_efficiency: Optional[float] = None
    self_discharge: Optional[float] = None
    cyclic_lifetime: Optional[int] = None
    charge_rate: Optional[float] = None
    discharge_rate: Optional[float] = None
    state_of_charge_min: Optional[float] = None
    state_of_charge_max: Optional[float] = None


class EnergyStorageCreate(EnergyStorageBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy storage.
    """
    pass


class EnergyStorageUpdate(EnergyStorageBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy storage.
    """
    commodity: Optional[str] = None


class EnergyStorage(EnergyStorageBase):
    """
    Properties to return via API for an energy storage.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
