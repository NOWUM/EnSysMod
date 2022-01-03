from typing import Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.util import validators


class EnergyStorageBase(BaseModel):
    """
    Shared properties for an energy storage. Used as a base class for all schemas.
    """   
    type = EnergyComponentType.STORAGE

    charge_efficiency: Optional[float] = None
    discharge_efficiency: Optional[float] = None
    self_discharge: Optional[float] = None
    cyclic_lifetime: Optional[int] = None
    charge_rate: Optional[float] = None
    discharge_rate: Optional[float] = None
    state_of_charge_min: Optional[float] = None
    state_of_charge_max: Optional[float] = None

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)
    
    _valid_charge_efficiency = validator("charge_efficiency", allow_reuse=True)(validators.validate_charge_efficiency)
    _valid_discharge_efficiency = validator("discharge_efficiency", allow_reuse=True)(validators.validate_discharge_efficiency)
    _valid_self_discharge = validator("self_discharge", allow_reuse=True)(validators.validate_self_discharge)
    _valid_cyclic_lifetime = validator("cyclic_lifetime", allow_reuse=True)(validators.validate_cyclic_lifetime)
    _valid_charge_rate = validator("charge_rate", allow_reuse=True)(validators.validate_charge_rate)
    _valid_discharge_rate = validator("discharge_rate", allow_reuse=True)(validators.validate_discharge_rate)
    _valid_state_of_charge_min = validator("state_of_charge_min", allow_reuse=True)(validators.validate_state_of_charge_min)
    _valid_state_of_charge_max = validator("state_of_charge_max", allow_reuse=True)(validators.validate_state_of_charge_max)
    


class EnergyStorageCreate(EnergyStorageBase, EnergyComponentCreate):
    """
    Properties to receive via API on creation of an energy storage.
    """
    commodity: str

     # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyStorageUpdate(EnergyStorageBase, EnergyComponentUpdate):
    """
    Properties to receive via API on update of an energy storage.
    """
    commodity: Optional[str] = None

     # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyStorage(EnergyStorageBase):
    """
    Properties to return via API for an energy storage.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
