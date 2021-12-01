from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType


class EnergyComponentBase(BaseModel):
    """
    Shared properties for an energy component. Used as a base class for all schemas.
    """
    name: str
    type: EnergyComponentType
    description: Optional[str] = None


class EnergyComponentCreate(EnergyComponentBase):
    """
    Properties to receive via API on creation of an energy component.
    """
    ref_dataset: int


class EnergyComponentUpdate(EnergyComponentBase):
    """
    Properties to receive via API on update of an energy component.
    """
    pass


# Additional properties to return via API
class EnergyComponent(EnergyComponentBase):
    """
    Properties to return via API for an energy component.
    """
    id: int

    class Config:
        orm_mode = True
