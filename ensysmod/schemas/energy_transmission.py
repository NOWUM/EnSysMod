from pydantic import Field, field_validator

from ensysmod.model import EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, ReturnSchema
from ensysmod.schemas.energy_commodity import EnergyCommodity
from ensysmod.schemas.energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
from ensysmod.utils import validators


class EnergyTransmissionBase(BaseSchema):
    """
    Shared attributes for an energy transmission. Used as a base class for all schemas.
    """

    type: EnergyComponentType = EnergyComponentType.TRANSMISSION

    # validators
    _valid_type = field_validator("type")(validators.validate_energy_component_type)


class EnergyTransmissionCreate(EnergyTransmissionBase, EnergyComponentCreate):
    """
    Attributes to receive via API on creation of an energy transmission.
    """

    commodity: str = Field(default=..., description="Commodity of energy transmission.", examples=["electricity"])

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergyTransmissionUpdate(EnergyTransmissionBase, EnergyComponentUpdate):
    """
    Attributes to receive via API on update of an energy transmission.
    """

    commodity: str | None = None

    # validators
    _valid_commodity = field_validator("commodity")(validators.validate_commodity)


class EnergyTransmission(EnergyTransmissionBase, ReturnSchema):
    """
    Attributes to return via API for an energy transmission.
    """

    component: EnergyComponent
    commodity: EnergyCommodity
