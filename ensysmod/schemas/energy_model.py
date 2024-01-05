from pydantic import BaseModel, Field, validator

from ensysmod.schemas import Dataset
from ensysmod.schemas.energy_model_optimization import (
    EnergyModelOptimization,
    EnergyModelOptimizationCreate,
    EnergyModelOptimizationUpdate,
)
from ensysmod.schemas.energy_model_override import (
    EnergyModelOverride,
    EnergyModelOverrideCreate,
    EnergyModelOverrideUpdate,
)
from ensysmod.utils import validators


class EnergyModelBase(BaseModel):
    """
    Shared attributes for an energy model. Used as a base class for all schemas.
    """

    name: str = Field(..., description="Name of the energy model.", example="100% CO2 reduction")

    description: str | None = Field(None, description="Description of the energy model", example="A model that reduces CO2 emissions by 100%")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyModelCreate(EnergyModelBase):
    """
    Attributes to receive via API on creation of an energy model.
    """

    ref_dataset: int = Field(..., description="ID of the dataset that the energy model is based on.", example=1)

    override_parameters: list[EnergyModelOverrideCreate] | None = Field(
        None,
        description="Override parameters of the energy model. If given, overrides the values of the referenced dataset.",
        example=[EnergyModelOverrideCreate(component="CO2 to environment", attribute="yearly_limit", operation="set", value=0)],
    )
    optimization_parameters: EnergyModelOptimizationCreate | None = Field(
        None,
        description="Optimization parameters of the energy model.",
        example=EnergyModelOptimizationCreate(
            start_year=2020,
            end_year=2050,
            number_of_steps=3,
            years_per_step=10,
            CO2_reference=366,
            CO2_reduction_targets=[0, 25, 50, 100],
        ),
    )

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyModelUpdate(EnergyModelBase):
    """
    Attributes to receive via API on update of an energy model.
    """

    name: str | None = None
    override_parameters: list[EnergyModelOverrideUpdate] | None = None
    optimization_parameters: list[EnergyModelOptimizationUpdate] | None = None


class EnergyModel(EnergyModelBase):
    """
    Attributes to return via API for an energy model.
    """

    id: int
    dataset: Dataset
    override_parameters: list[EnergyModelOverride]
    optimization_parameters: list[EnergyModelOptimization]

    class Config:
        orm_mode = True
