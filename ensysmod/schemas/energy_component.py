from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.model import EnergyComponentType, CapacityVariableDomain
from ensysmod.util import validators


class EnergyComponentBase(BaseModel):
    """
    Shared properties for an energy component. Used as a base class for all schemas.
    """
    name: str
    description: Optional[str] = None

    capacity_variable: Optional[bool] = None
    capacity_variable_domain: Optional[CapacityVariableDomain] = None
    capacity_per_plant_unit: Optional[float] = None

    invest_per_capacity: Optional[float] = None
    opex_per_capacity: Optional[float] = None
    interest_rate: Optional[float] = None
    economic_lifetime: Optional[int] = None

    shared_potential_id: Optional[str] = None

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyComponentCreate(EnergyComponentBase):
    """
    Properties to receive via API on creation of an energy component.
    """
    ref_dataset: int
    type: EnergyComponentType

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)


class EnergyComponentUpdate(EnergyComponentBase):
    """
    Properties to receive via API on update of an energy component.
    """
    name: Optional[str] = None


class EnergyComponent(EnergyComponentBase):
    """
    Properties to return via API for an energy component.
    """
    id: int
    type: EnergyComponentType

    class Config:
        orm_mode = True
