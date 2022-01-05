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
    _valid_capacity_per_plant_unit = validator("capacity_per_plant_unit", allow_reuse=True)(validators.validate_capacity_per_plant_unit)
    _valid_invest_per_capacity = validator("invest_per_capacity", allow_reuse=True)(validators.validate_invest_per_capacity)
    _valid_opex_per_capacity = validator("opex_per_capacity", allow_reuse=True)(validators.validate_opex_per_capacity)
    _valid_interest_rate = validator("interest_rate", allow_reuse=True)(validators.validate_interest_rate)
    _valid_economic_lifetime = validator("economic_lifetime", allow_reuse=True)(validators.validate_economic_lifetime)
    _valid_shared_potential_id = validator("shared_potential_id", allow_reuse=True)(validators.validate_shared_potential_id)

class EnergyComponentCreate(EnergyComponentBase):
    """
    Properties to receive via API on creation of an energy component.
    """
    ref_dataset: int
    type: EnergyComponentType

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)
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
