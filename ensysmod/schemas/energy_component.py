from typing import Optional

from pydantic import BaseModel

from ensysmod.model import EnergyComponentType, CapacityVariableDomain


class EnergyComponentBase(BaseModel):
    """
    Shared properties for an energy component. Used as a base class for all schemas.
    """
    name: str
    type: EnergyComponentType
    description: Optional[str] = None

    capacity_variable: Optional[bool] = None
    capacity_variable_domain: Optional[CapacityVariableDomain] = None
    capacity_per_plant_unit: Optional[float] = None

    invest_per_capacity: Optional[float] = None
    opex_per_capacity: Optional[float] = None
    interest_rate: Optional[float] = None
    economic_lifetime: Optional[int] = None


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


class EnergyComponent(EnergyComponentBase):
    """
    Properties to return via API for an energy component.
    """
    id: int

    class Config:
        orm_mode = True
