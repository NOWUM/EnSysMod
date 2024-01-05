from pydantic import BaseModel, Field, validator

from ensysmod.model import CapacityVariableDomain, EnergyComponentType
from ensysmod.utils import validators


class EnergyComponentBase(BaseModel):
    """
    Shared attributes for an energy component. Used as a base class for all schemas.
    """

    name: str = Field(..., description="Unique name of the energy component. It is used to identify the component.", example="gas turbine")

    description: str | None = Field(None, description="Description of the energy component. Can be used to explain the component.")

    capacity_variable: bool | None = Field(None, description="Whether the energy component should be model with a capacity or not.")

    capacity_variable_domain: CapacityVariableDomain | None = Field(
        None,
        description="Mathematical domain of the capacity variables. 'continuous' means that the capacity is modeled as real values >= 0. 'discrete' means that the capacity is modeled as integer values >= 0.",  # noqa: E501
    )

    capacity_per_plant_unit: float | None = Field(
        None,
        description="Capacity per plant unit. By default is 1, thus the number of plants is the equal to the installed capacity.",
    )

    invest_per_capacity: float | None = Field(None, description="Investment per capacity.")

    opex_per_capacity: float | None = Field(None, description="Operational expenditure per capacity.")

    interest_rate: float | None = Field(None, description="Interest rate.")

    economic_lifetime: int | None = Field(None, description="Economic lifetime.")

    shared_potential_id: str | None = Field(
        None,
        description="Shared potential ID. If specified, the maximum potential capacity is shared among all components of the same shared potential id.",  # noqa: E501
    )
    linked_quantity_id: str | None = Field(
        None,
        description="Linked quantity ID. If specified, components of the same linked quantity ID are built with the same quantity.",
    )

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)
    _valid_capacity_per_plant_unit = validator("capacity_per_plant_unit", allow_reuse=True)(validators.validate_capacity_per_plant_unit)
    _valid_invest_per_capacity = validator("invest_per_capacity", allow_reuse=True)(validators.validate_invest_per_capacity)
    _valid_opex_per_capacity = validator("opex_per_capacity", allow_reuse=True)(validators.validate_opex_per_capacity)
    _valid_interest_rate = validator("interest_rate", allow_reuse=True)(validators.validate_interest_rate)
    _valid_economic_lifetime = validator("economic_lifetime", allow_reuse=True)(validators.validate_economic_lifetime)
    _valid_shared_potential_id = validator("shared_potential_id", allow_reuse=True)(validators.validate_shared_potential_id)
    _valid_linked_quantity_id = validator("linked_quantity_id", allow_reuse=True)(validators.validate_linked_quantity_id)


class EnergyComponentCreate(EnergyComponentBase):
    """
    Attributes to receive via API on creation of an energy component.
    """

    ref_dataset: int = Field(..., description="Reference to dataset that energy component belongs to.", example=1)

    type: EnergyComponentType = Field(..., description="Type of the energy component.")

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)
    _valid_type = validator("type", allow_reuse=True)(validators.validate_energy_component_type)


class EnergyComponentUpdate(EnergyComponentBase):
    """
    Attributes to receive via API on update of an energy component.
    """

    name: str | None = None


class EnergyComponent(EnergyComponentBase):
    """
    Attributes to return via API for an energy component.
    """

    id: int = Field(..., description="The unique ID of the energy component.")
    type: EnergyComponentType = Field(..., description="Type of the energy component.")

    class Config:
        orm_mode = True
