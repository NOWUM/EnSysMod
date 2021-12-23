from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.model import EnergyComponentType, CapacityVariableDomain


class EnergyComponentBase(BaseModel):
    """
    Shared properties for an energy component. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the energy component", example="component_name")
    type: EnergyComponentType = Field(..., description="Type of the energy component")
    description: Optional[str] = Field(None, description="Description of the energy component")

    capacity_variable: Optional[bool] = Field(None, description="Whether the energy component has a variable capacity")
    capacity_variable_domain: Optional[CapacityVariableDomain] \
        = Field(None, description="Domain of the capacity variable")
    capacity_per_plant_unit: Optional[float] = Field(None, description="Capacity per plant unit")

    invest_per_capacity: Optional[float] = Field(None, description="Investment per capacity")
    opex_per_capacity: Optional[float] = Field(None, description="Operational expenditure per capacity")
    interest_rate: Optional[float] = Field(None, description="Interest rate")
    economic_lifetime: Optional[int] = Field(None, description="Economic lifetime")

    shared_potential_id: Optional[str] = Field(None, description="Shared potential ID")


class EnergyComponentCreate(EnergyComponentBase):
    """
    Properties to receive via API on creation of an energy component.
    """
    ref_dataset: int = Field(..., description="Reference dataset", example=1)


class EnergyComponentUpdate(EnergyComponentBase):
    """
    Properties to receive via API on update of an energy component.
    """
    pass


class EnergyComponent(EnergyComponentBase):
    """
    Properties to return via API for an energy component.
    """
    id: int = Field(..., description="ID of the energy component")

    class Config:
        orm_mode = True
