from pydantic import Field, model_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.utils import validators


class EnergyModelOptimizationBase(BaseSchema):
    """
    Shared attributes for a model optimization parameter. Used as a base class for all schemas.
    """

    start_year: int = Field(
        default=...,
        description="Year of the first optimization",
        examples=[2020],
        ge=0,
    )
    end_year: int | None = Field(
        default=None,
        description="Year of the last optimization",
        examples=[2050],
    )
    number_of_steps: int | None = Field(
        default=None,
        description="Number of optimization runs excluding the start year",
        examples=[3],
    )
    years_per_step: int | None = Field(
        default=None,
        description="Number of years represented by one optimization run",
        examples=[10],
    )
    CO2_reference: float | None = Field(
        default=None,
        description="CO2 emission reference value to which the reduction should be applied to",
        examples=[366],
        ge=0,
    )
    CO2_reduction_targets: list[float] | None = Field(
        default=None,
        description="CO2 reduction targets for all optimization periods, in percentages. If specified, the length of the list must equal the number of optimization steps, and a sink component named 'CO2 to environment' is required.",  # noqa: E501
        examples=[[0, 25, 50, 100]],
    )

    # validators
    _valid_optimization_timeframe = model_validator(mode="after")(validators.validate_optimization_timeframe)
    _valid_CO2_optimization = model_validator(mode="after")(validators.validate_CO2_optimization)


class EnergyModelOptimizationCreate(EnergyModelOptimizationBase, CreateSchema):
    """
    Attributes to receive via API on creation of a model optimization parameter.
    """

    ref_model: int | None = Field(
        default=None,
        description="The ID of the referenced model. Current model is used as default.",
        gt=0,
    )


class EnergyModelOptimizationUpdate(EnergyModelOptimizationBase, UpdateSchema):
    """
    Attributes to receive via API on update of a model optimization parameter.
    """

    start_year: int | None = None
    end_year: int | None = None
    number_of_steps: int | None = None
    years_per_step: int | None = None
    CO2_reference: float | None = None
    CO2_reduction_target: list[float] | None = None

    # validators
    _valid_optimization_timeframe = model_validator(mode="after")(validators.validate_optimization_timeframe)
    _valid_CO2_optimization = model_validator(mode="after")(validators.validate_CO2_optimization)


class EnergyModelOptimization(EnergyModelOptimizationBase, ReturnSchema):
    """
    Attributes to return via API for a model optimization parameter.
    """

    ref_model: int
