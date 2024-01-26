from pydantic import Field

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommoditySchema
from ensysmod.schemas.energy_component import EnergyComponentCreate, EnergyComponentSchema, EnergyComponentUpdate


class EnergyTransmissionBase(BaseSchema):
    """
    Shared attributes for an energy transmission. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.TRANSMISSION


class EnergyTransmissionCreate(EnergyTransmissionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy transmission.
    """

    commodity: str = Field(
        default=...,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyTransmissionUpdate(EnergyTransmissionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy transmission.
    """

    commodity: str | None = Field(
        default=None,
        description="Commodity the energy sink is based on.",
        examples=["electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyTransmissionSchema(EnergyTransmissionBase, ReturnSchema):
    """
    Attributes to return via API for an energy transmission.
    """

    component: EnergyComponentSchema
    commodity: EnergyCommoditySchema
