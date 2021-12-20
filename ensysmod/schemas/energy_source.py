from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity


class EnergySourceBase(BaseModel):
    """
    Shared properties for an energy source. Used as a base class for all schemas.
    """
    commodity: str
    type = EnergyComponentType.SOURCE
    commodity_cost: Optional[float] = None


class EnergySourceCreate(EnergySourceBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy source.
    """
    pass


class EnergySourceUpdate(EnergySourceBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy source.
    """
    commodity: Optional[str] = None


class EnergySource(EnergySourceBase):
    """
    Properties to return via API for an energy source.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
