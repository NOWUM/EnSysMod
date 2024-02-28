from pydantic import Field

from ensysmod.model import EnergyModelOverrideAttribute, EnergyModelOverrideOperation
from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema


class EnergyModelOverrideBase(BaseSchema):
    """
    Shared attributes for a model parameter override. Used as a base class for all schemas.
    """

    attribute: EnergyModelOverrideAttribute = Field(
        default=...,
        description="The attribute of the component to be overridden.",
        examples=[EnergyModelOverrideAttribute.yearlyLimit],
    )
    operation: EnergyModelOverrideOperation = Field(
        default=...,
        description="The operation of the override. Input should be 'set', 'add' or 'multiply'.",
        examples=[EnergyModelOverrideOperation.set],
    )
    value: float = Field(default=..., description="The value of the parameter.", examples=[-5.5])


class EnergyModelOverrideCreate(EnergyModelOverrideBase, CreateSchema):
    """
    Attributes to receive via API on creation of a model parameter override.
    """

    component_name: str = Field(
        default=...,
        description="The name of the component which attribute is overridden.",
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyModelOverrideUpdate(EnergyModelOverrideBase, UpdateSchema):
    """
    Attributes to receive via API on update of a model parameter override.
    """

    attribute: EnergyModelOverrideAttribute | None = None
    operation: EnergyModelOverrideOperation | None = None
    value: float | None = None


class EnergyModelOverrideSchema(EnergyModelOverrideBase, ReturnSchema):
    """
    Attributes to return via API for a model parameter override.
    """

    id: int
