from typing import List, Optional

from pydantic import BaseModel, Field, root_validator

from ensysmod.utils import validators


class EnergyModelOptimizationBase(BaseModel):
    """
    Shared attributes for a model optimization parameter. Used as a base class for all schemas.
    """
    start_year: int = Field(..., description="Year of the first optimization", example="2020")
    end_year: Optional[int] = Field(None, description="Year of the last optimization", example="2050")
    number_of_steps: Optional[int] = Field(None, description="Number of optimization runs excluding the start year", example="3")
    years_per_step: Optional[int] = Field(None, description="Number of years represented by one optimization run", example="10")
    CO2_reference: Optional[float] = Field(
        None,
        description="CO2 emission reference value to which the reduction should be applied to",
        example="366",
    )
    CO2_reduction_targets: Optional[List[float]] = Field(
        None,
        description="CO2 reduction targets for all optimization periods, in percentages. If specified, the length of the list must equal the number of optimization steps, and a sink component named 'CO2 to environment' is required.",  # noqa: E501
        example="[0, 25, 50, 100]",
    )

    # validators
    _valid_optimization_timeframe = root_validator(allow_reuse=True)(validators.validate_optimization_timeframe)
    _valid_CO2_optimization = root_validator(allow_reuse=True)(validators.validate_CO2_optimization)


class EnergyModelOptimizationCreate(EnergyModelOptimizationBase):
    """
    Attributes to receive via API on creation of a model optimization parameter.
    """
    ref_model: Optional[int] = None


class EnergyModelOptimizationUpdate(EnergyModelOptimizationBase):
    """
    Attributes to receive via API on update of a model optimization parameter.
    """
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    number_of_steps: Optional[int] = None
    years_per_step: Optional[int] = None
    CO2_reference: Optional[float] = None
    CO2_reduction_target: Optional[List[float]] = None

    # validators
    _valid_optimization_timeframe = root_validator(allow_reuse=True)(validators.validate_optimization_timeframe)
    _valid_CO2_optimization = root_validator(allow_reuse=True)(validators.validate_CO2_optimization)


class EnergyModelOptimization(EnergyModelOptimizationBase):
    """
    Attributes to return via API for a model optimization parameter.
    """
    ref_model: int

    class Config:
        orm_mode = True
