from pydantic import Field

from ensysmod.model import CapacityVariableDomain, EnergyComponentType
from ensysmod.schemas.base_schema import MAX_DESC_LENGTH, MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema


class EnergyComponentBase(BaseSchema):
    """
    Shared attributes for an energy component. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="Unique name of the energy component. It is used to identify the component.",
        examples=["gas turbine"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    description: str | None = Field(
        default=None,
        description="Description of the energy component. Can be used to explain the component.",
        max_length=MAX_DESC_LENGTH,
    )
    capacity_variable: bool | None = Field(
        default=False,
        description="Whether the energy component should be model with a capacity or not.",
    )
    capacity_variable_domain: CapacityVariableDomain | None = Field(
        default=CapacityVariableDomain.CONTINUOUS,
        description="Mathematical domain of the capacity variables. 'continuous' means that the capacity is modeled as real values >= 0. 'discrete' means that the capacity is modeled as integer values >= 0.",  # noqa: E501
    )
    capacity_per_plant_unit: float | None = Field(
        default=1.0,
        description="Capacity per plant unit. By default is 1, thus the number of plants is the equal to the installed capacity.",
        gt=0,
    )
    invest_per_capacity: float | None = Field(
        default=0.0,
        description="Investment per capacity.",
        ge=0,
    )
    opex_per_capacity: float | None = Field(
        default=0.0,
        description="Operational expenditure per capacity.",
        ge=0,
    )
    interest_rate: float | None = Field(
        default=0.08,
        description="Interest rate.",
        ge=0,
        le=1,
    )
    economic_lifetime: int | None = Field(
        default=10,
        description="Economic lifetime.",
        gt=0,
    )
    shared_potential_id: str | None = Field(
        default=None,
        description="Shared potential ID. If specified, the maximum potential capacity is shared among all components of the same shared potential id.",  # noqa: E501
        max_length=MAX_STR_LENGTH,
    )
    linked_quantity_id: str | None = Field(
        default=None,
        description="Linked quantity ID. If specified, components of the same linked quantity ID are built with the same quantity.",
        max_length=MAX_STR_LENGTH,
    )


class EnergyComponentCreate(EnergyComponentBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy component.
    """

    ref_dataset: int = Field(
        default=...,
        description="Reference to dataset that energy component belongs to.",
        examples=[1],
        gt=0,
    )
    type: EnergyComponentType = Field(
        default=...,
        description="Type of the energy component. Input should be 'SOURCE', 'SINK', 'CONVERSION', 'TRANSMISSION' or 'STORAGE'.",
        examples=[EnergyComponentType.SOURCE],
    )


class EnergyComponentUpdate(EnergyComponentBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy component.
    """

    name: str | None = Field(
        default=None,
        description="Unique name of the energy component. It is used to identify the component.",
        examples=["gas turbine"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyComponentSchema(EnergyComponentBase, ReturnSchema):
    """
    Attributes to return via API for an energy component.
    """

    id: int
    type: EnergyComponentType
