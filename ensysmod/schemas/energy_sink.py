from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate, EnergyComponent, EnergyCommodity


class EnergySinkBase(BaseModel):
    """
    Shared properties for an energy sink. Used as a base class for all schemas.
    """
    commodity: str
    type = EnergyComponentType.SINK


class EnergySinkCreate(EnergySinkBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy sink.
    """
    pass


class EnergySinkUpdate(EnergySinkBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy sink.
    """
    commodity: Optional[str] = None


class EnergySink(EnergySinkBase):
    """
    Properties to return via API for an energy sink.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
