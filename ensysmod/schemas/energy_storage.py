from pydantic import Field, field_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
from ensysmod.utils import validators


class EnergyStorageBase(BaseSchema):
    """
    Shared attributes for an energy storage. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.STORAGE

    charge_efficiency: float | None = Field(default=None, description="The efficiency of charging the storage.", examples=[0.9])
    discharge_efficiency: float | None = Field(default=None, description="The efficiency of discharging the storage.", examples=[0.9])
    self_discharge: float | None = Field(default=None, description="The self-discharge of the storage.", examples=[0.00009])
    cyclic_lifetime: int | None = Field(default=None, description="The cyclic lifetime of the storage.", examples=[100])
    charge_rate: float | None = Field(default=None, description="The charge rate of the storage.", examples=[0.3])
    discharge_rate: float | None = Field(default=None, description="The discharge rate of the storage.", examples=[0.2])
    state_of_charge_min: float | None = Field(default=None, description="The minimum state of charge of the storage.", examples=[0.1])
    state_of_charge_max: float | None = Field(default=None, description="The maximum state of charge of the storage.", examples=[0.9])

    # validators
    _valid_type = field_validator("type")(validators.validate_energy_component_type)

    _valid_charge_efficiency = field_validator("charge_efficiency")(validators.validate_charge_efficiency)
    _valid_discharge_efficiency = field_validator("discharge_efficiency")(validators.validate_discharge_efficiency)
    _valid_self_discharge = field_validator("self_discharge")(validators.validate_self_discharge)
    _valid_cyclic_lifetime = field_validator("cyclic_lifetime")(validators.validate_cyclic_lifetime)
    _valid_charge_rate = field_validator("charge_rate")(validators.validate_charge_rate)
    _valid_discharge_rate = field_validator("discharge_rate")(validators.validate_discharge_rate)
    _valid_state_of_charge_min = field_validator("state_of_charge_min")(validators.validate_state_of_charge_min)
    _valid_state_of_charge_max = field_validator("state_of_charge_max")(validators.validate_state_of_charge_max)


class EnergyStorageCreate(EnergyStorageBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy storage.
    """

    commodity: str = Field(default=..., description="Commodity to be stored in the energy storage.", examples=["electricity"])

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergyStorageUpdate(EnergyStorageBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy storage.
    """

    commodity: str | None = None

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergyStorage(EnergyStorageBase, ReturnSchema):
    """
    Attributes to return via API for an energy storage.
    """

    component: EnergyComponent
    commodity: EnergyCommodity
