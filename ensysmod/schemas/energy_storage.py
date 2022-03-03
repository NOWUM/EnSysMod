from typing import Optional

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas import EnergyComponentCreate, EnergyComponent, EnergyComponentUpdate, EnergyCommodity
from ensysmod.util import validators


class EnergyStorageBase(BaseModel):
    """
    Shared attributes for an energy storage. Used as a base class for all schemas.
    """
    type = EnergyComponentType.STORAGE

    charge_efficiency: Optional[float] = Field(None,
                                               description="The efficiency of charging the storage.", example=0.9)
    discharge_efficiency: Optional[float] = Field(None,
                                                  description="The efficiency of discharging the storage.", example=0.9)
    self_discharge: Optional[float] = Field(None,
                                            description="The self-discharge of the storage.", example=0.00009)
    cyclic_lifetime: Optional[int] = Field(None,
                                           description="The cyclic lifetime of the storage.", example=100)
    charge_rate: Optional[float] = Field(None,
                                         description="The charge rate of the storage.", example=0.3)
    discharge_rate: Optional[float] = Field(None,
                                            description="The discharge rate of the storage.", example=0.2)
    state_of_charge_min: Optional[float] = Field(None,
                                                 description="The minimum state of charge of the storage.", example=0.1)
    state_of_charge_max: Optional[float] = Field(None,
                                                 description="The maximum state of charge of the storage.", example=0.9)

    # validators
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)

    _valid_charge_efficiency = validator("charge_efficiency", allow_reuse=True)(validators.validate_charge_efficiency)
    _valid_discharge_efficiency = validator("discharge_efficiency", allow_reuse=True)(
        validators.validate_discharge_efficiency)
    _valid_self_discharge = validator("self_discharge", allow_reuse=True)(validators.validate_self_discharge)
    _valid_cyclic_lifetime = validator("cyclic_lifetime", allow_reuse=True)(validators.validate_cyclic_lifetime)
    _valid_charge_rate = validator("charge_rate", allow_reuse=True)(validators.validate_charge_rate)
    _valid_discharge_rate = validator("discharge_rate", allow_reuse=True)(validators.validate_discharge_rate)
    _valid_state_of_charge_min = validator("state_of_charge_min", allow_reuse=True)(
        validators.validate_state_of_charge_min)
    _valid_state_of_charge_max = validator("state_of_charge_max", allow_reuse=True)(
        validators.validate_state_of_charge_max)


class EnergyStorageCreate(EnergyStorageBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy storage.
    """
    commodity: str = Field(...,
                           description="Commodity to be stored in the energy storage.",
                           example="electricity")

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyStorageUpdate(EnergyStorageBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy storage.
    """
    commodity: Optional[str] = None

    # validators
    _valid_commodity = validator("commodity", allow_reuse=True)(validators.validate_commodity)


class EnergyStorage(EnergyStorageBase):
    """
    Attributes to return via API for an energy storage.
    """
    component: EnergyComponent
    commodity: EnergyCommodity

    class Config:
        orm_mode = True
