from pydantic import Field

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate


class EnergyStorageBase(BaseSchema):
    """
    Shared attributes for an energy storage. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.STORAGE

    charge_efficiency: float | None = Field(
        default=None,
        description="The efficiency of charging the storage.",
        examples=[0.9],
        ge=0,
        le=1,
    )
    discharge_efficiency: float | None = Field(
        default=None,
        description="The efficiency of discharging the storage.",
        examples=[0.9],
        ge=0,
        le=1,
    )
    self_discharge: float | None = Field(
        default=None,
        description="The self-discharge of the storage.",
        examples=[0.00009],
        ge=0,
        le=1,
    )
    cyclic_lifetime: int | None = Field(
        default=None,
        description="The cyclic lifetime of the storage.",
        examples=[100],
        gt=0,
    )
    charge_rate: float | None = Field(
        default=None,
        description="The charge rate of the storage.",
        examples=[0.3],
        ge=0,
        le=1,
    )
    discharge_rate: float | None = Field(
        default=None,
        description="The discharge rate of the storage.",
        examples=[0.2],
        ge=0,
        le=1,
    )
    state_of_charge_min: float | None = Field(
        default=None,
        description="The minimum state of charge of the storage.",
        examples=[0.1],
        ge=0,
        le=1,
    )
    state_of_charge_max: float | None = Field(
        default=None,
        description="The maximum state of charge of the storage.",
        examples=[0.9],
        ge=0,
        le=1,
    )


class EnergyStorageCreate(EnergyStorageBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy storage.
    """

    commodity: str = Field(
        default=...,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyStorageUpdate(EnergyStorageBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy storage.
    """

    commodity: str | None = Field(
        default=None,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyStorage(EnergyStorageBase, ReturnSchema):
    """
    Attributes to return via API for an energy storage.
    """

    component: EnergyComponent
    commodity: EnergyCommodity
