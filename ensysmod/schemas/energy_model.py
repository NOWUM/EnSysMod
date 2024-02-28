from pydantic import Field

from ensysmod.model import EnergyModelOverrideAttribute, EnergyModelOverrideOperation
from ensysmod.schemas.base_schema import MAX_DESC_LENGTH, MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import DatasetSchema
from ensysmod.schemas.energy_model_optimization import EnergyModelOptimizationCreate, EnergyModelOptimizationSchema
from ensysmod.schemas.energy_model_override import EnergyModelOverrideCreate, EnergyModelOverrideSchema


class EnergyModelBase(BaseSchema):
    """
    Shared attributes for an energy model. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="Name of the energy model.",
        examples=["100% CO2 reduction"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    description: str | None = Field(
        default=None,
        description="Description of the energy model",
        examples=["A model that reduces CO2 emissions by 100%"],
        max_length=MAX_DESC_LENGTH,
    )


class EnergyModelCreate(EnergyModelBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy model.
    """

    ref_dataset: int = Field(
        default=...,
        description="ID of the dataset that the energy model is based on.",
        examples=[1],
        gt=0,
    )
    override_parameters: list[EnergyModelOverrideCreate] = Field(
        default=[],
        description="Override parameters of the energy model. If given, overrides the values of the referenced dataset.",
        examples=[
            [
                EnergyModelOverrideCreate(
                    component_name="CO2 to environment",
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


class EnergyModelUpdate(EnergyModelBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy model.
    """

    name: str | None = Field(
        default=None,
        description="Name of the energy model.",
        examples=["100% CO2 reduction"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class EnergyModelSchema(EnergyModelBase, ReturnSchema):
    """
    Attributes to return via API for an energy model.
    """

    id: int
    dataset: DatasetSchema
    override_parameters: list[EnergyModelOverrideSchema] | None
    optimization_parameters: EnergyModelOptimizationSchema | None
