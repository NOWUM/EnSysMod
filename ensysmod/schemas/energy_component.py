from pydantic import Field, field_validator

from ensysmod.model import CapacityVariableDomain, EnergyComponentType
from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.utils import validators


class EnergyComponentBase(BaseSchema):
    """
    Shared attributes for an energy component. Used as a base class for all schemas.
    """

    name: str = Field(default=..., description="Unique name of the energy component. It is used to identify the component.", examples=["gas turbine"])
    description: str | None = Field(default=None, description="Description of the energy component. Can be used to explain the component.")
    capacity_variable: bool | None = Field(default=None, description="Whether the energy component should be model with a capacity or not.")
    capacity_variable_domain: CapacityVariableDomain | None = Field(
        default=None,
        description="Mathematical domain of the capacity variables. 'continuous' means that the capacity is modeled as real values >= 0. 'discrete' means that the capacity is modeled as integer values >= 0.",  # noqa: E501
    )
    capacity_per_plant_unit: float | None = Field(
        default=None,
        description="Capacity per plant unit. By default is 1, thus the number of plants is the equal to the installed capacity.",
    )
    invest_per_capacity: float | None = Field(default=None, description="Investment per capacity.")
    opex_per_capacity: float | None = Field(default=None, description="Operational expenditure per capacity.")
    interest_rate: float | None = Field(default=None, description="Interest rate.")
    economic_lifetime: int | None = Field(default=None, description="Economic lifetime.")
    shared_potential_id: str | None = Field(
        default=None,
        description="Shared potential ID. If specified, the maximum potential capacity is shared among all components of the same shared potential id.",  # noqa: E501
    )
    linked_quantity_id: str | None = Field(
        default=None,
        description="Linked quantity ID. If specified, components of the same linked quantity ID are built with the same quantity.",
    )

    # validators
    _valid_name = field_validator("name")(validators.validate_name)
    _valid_description = field_validator("description")(validators.validate_description)
    _valid_capacity_per_plant_unit = field_validator("capacity_per_plant_unit")(validators.validate_capacity_per_plant_unit)
    _valid_invest_per_capacity = field_validator("invest_per_capacity")(validators.validate_invest_per_capacity)
    _valid_opex_per_capacity = field_validator("opex_per_capacity")(validators.validate_opex_per_capacity)
    _valid_interest_rate = field_validator("interest_rate")(validators.validate_interest_rate)
    _valid_economic_lifetime = field_validator("economic_lifetime")(validators.validate_economic_lifetime)
    _valid_shared_potential_id = field_validator("shared_potential_id")(validators.validate_shared_potential_id)
    _valid_linked_quantity_id = field_validator("linked_quantity_id")(validators.validate_linked_quantity_id)


class EnergyComponentCreate(EnergyComponentBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy component.
    """

    ref_dataset: int = Field(default=..., description="Reference to dataset that energy component belongs to.", examples=[1])
    type: EnergyComponentType = Field(default=..., description="Type of the energy component.")

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_required)
    _valid_type = field_validator("type")(validators.validate_energy_component_type)


class EnergyComponentUpdate(EnergyComponentBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy component.
    """

    name: str | None = None


class EnergyComponent(EnergyComponentBase, ReturnSchema):
    """
    Attributes to return via API for an energy component.
    """

    id: int = Field(default=..., description="The unique ID of the energy component.")
    type: EnergyComponentType = Field(default=..., description="Type of the energy component.")
