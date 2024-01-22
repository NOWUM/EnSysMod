from pydantic import Field, field_validator

from ensysmod.model.energy_model_override import EnergyModelOverrideAttribute, EnergyModelOverrideOperation
from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import Dataset
from ensysmod.schemas.energy_model_optimization import EnergyModelOptimization, EnergyModelOptimizationCreate, EnergyModelOptimizationUpdate
from ensysmod.schemas.energy_model_override import EnergyModelOverride, EnergyModelOverrideCreate, EnergyModelOverrideUpdate
from ensysmod.utils import validators


class EnergyModelBase(BaseSchema):
    """
    Shared attributes for an energy model. Used as a base class for all schemas.
    """

    name: str = Field(default=..., description="Name of the energy model.", examples=["100% CO2 reduction"])

    description: str | None = Field(
        default=None, description="Description of the energy model", examples=["A model that reduces CO2 emissions by 100%"]
    )

    # validators
    _valid_name = field_validator("name")(validators.validate_name)
    _valid_description = field_validator("description")(validators.validate_description)


class EnergyModelCreate(EnergyModelBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy model.
    """

    ref_dataset: int = Field(default=..., description="ID of the dataset that the energy model is based on.", examples=[1])

    override_parameters: list[EnergyModelOverrideCreate] | None = Field(
        default=None,
        description="Override parameters of the energy model. If given, overrides the values of the referenced dataset.",
        examples=[
            [
                EnergyModelOverrideCreate(
                    component="CO2 to environment",
                    attribute=EnergyModelOverrideAttribute.yearlyLimit,
                    operation=EnergyModelOverrideOperation.set,
                    value=0,
                )
            ]
        ],
    )
    optimization_parameters: EnergyModelOptimizationCreate | None = Field(
        default=None,
        description="Optimization parameters of the energy model.",
        examples=[
            EnergyModelOptimizationCreate(
                start_year=2020,
                end_year=2050,
                number_of_steps=3,
                years_per_step=10,
                CO2_reference=366,
                CO2_reduction_targets=[0, 25, 50, 100],
            )
        ],
    )

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_required)


class EnergyModelUpdate(EnergyModelBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy model.
    """

    name: str | None = None
    override_parameters: list[EnergyModelOverrideUpdate] | None = None
    optimization_parameters: list[EnergyModelOptimizationUpdate] | None = None


class EnergyModel(EnergyModelBase, ReturnSchema):
    """
    Attributes to return via API for an energy model.
    """

    id: int
    dataset: Dataset
    override_parameters: list[EnergyModelOverride]
    optimization_parameters: list[EnergyModelOptimization]
