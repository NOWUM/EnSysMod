from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ensysmod.schemas.energy_model_optimization import EnergyModelOptimizationBase
    from ensysmod.schemas.energy_sink import EnergySinkBase
    from ensysmod.schemas.energy_source import EnergySourceBase


def validate_conversion_factors(conversion_factors: list[Any]) -> list[Any]:
    """
    Validates the conversion factors of an object.

    :param conversion_factors: The conversion_factor of the object.
    :return: The validated conversion_factor.
    """
    if len(conversion_factors) == 0:
        raise ValueError("List of conversion factors should not be empty")
    return conversion_factors


def validate_yearly_limit_and_commodity_limit_id(model: EnergySourceBase | EnergySinkBase) -> EnergySourceBase | EnergySinkBase:
    """
    Validates the yearly limit and the commodity limit ID of an object.

    :param yearly_limit: The yearly limit of the object.
    :param commodity_limit_id: The commodity limit id of the object.
    :return: The validated yearly limit and commodity limit id.
    """
    yearly_limit, commodity_limit_id = model.yearly_limit, model.commodity_limit_id

    if yearly_limit is None and commodity_limit_id is None:
        # Skip validation if no value provided
        return model
    if yearly_limit is not None and commodity_limit_id is None:
        raise ValueError("If yearly_limit is specified, commodity_limit_id must be specified as well.")
    return model


def validate_optimization_timeframe(model: EnergyModelOptimizationBase) -> EnergyModelOptimizationBase:
    """
    Validates the optimization timeframe of an object.

    :param start_year: Year of the first optimization.
    :param end_year: Year of the last optimization.
    :param number_of_steps: Number of optimization runs excluding the start year.
    :param years_per_step: Number of years represented by one optimization run.

    :return: the validated optimization timeframe parameters.
    """
    start_year = model.start_year
    end_year = model.end_year
    number_of_steps = model.number_of_steps
    years_per_step = model.years_per_step

    if (end_year is None) & (number_of_steps is None) & (years_per_step is None):
        raise ValueError("At least two of the parameters end_year, number_of_steps or years_per_step must be specified.")

    if (end_year is not None) & (number_of_steps is None) & (years_per_step is None):
        raise ValueError("At least one of the parameters number_of_steps or years_per_step must also be specified.")
    if (end_year is None) & (number_of_steps is not None) & (years_per_step is None):
        raise ValueError("At least one of the parameters end_year or years_per_step must also be specified.")
    if (end_year is None) & (number_of_steps is None) & (years_per_step is not None):
        raise ValueError("At least one of the parameters end_year or number_of_steps must also be specified.")

    if (end_year is None) & (number_of_steps is not None) & (years_per_step is not None):
        end_year = start_year + number_of_steps * years_per_step
    elif (end_year is not None) & (number_of_steps is None) & (years_per_step is not None):
        number_of_steps = (end_year - start_year) / years_per_step
    elif (end_year is not None) & (number_of_steps is not None) & (years_per_step is None):
        years_per_step = (end_year - start_year) / number_of_steps

    if (end_year - start_year) != number_of_steps * years_per_step:
        raise ValueError("The parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step.")

    model.end_year = end_year
    model.number_of_steps = number_of_steps
    model.years_per_step = years_per_step

    return model


def validate_CO2_optimization(model: EnergyModelOptimizationBase) -> EnergyModelOptimizationBase:
    """
    Validates the CO2 optimization.

    :param CO2_reference: CO2 emission reference value to which the reduction should be applied to.
    :param CO2_reduction_targets: CO2 reduction targets for all optimization periods, in percentages. If specified, the length of the list must equal the number of optimization steps.

    :return: The validated CO2 optimization parameters.
    """  # noqa: E501
    CO2_reference = model.CO2_reference
    CO2_reduction_targets = model.CO2_reduction_targets
    number_of_steps = model.number_of_steps

    if CO2_reference is None and CO2_reduction_targets is None:
        return model
    if CO2_reference is not None and CO2_reduction_targets is None:
        raise ValueError("If CO2_reference is specified, CO2_reduction_targets must also be specified.")
    if CO2_reference is None and CO2_reduction_targets is not None:
        raise ValueError("If CO2_reduction_targets is specified, CO2_reference must also be specified.")

    for target in CO2_reduction_targets:
        if target < 0 or target > 100:
            raise ValueError("Values of CO2_reduction_targets must be between 0 and 100.")

    if len(CO2_reduction_targets) != number_of_steps + 1:
        raise ValueError(
            f"The number of values given in CO2_reduction_targets must match the number of optimization runs. Expected: {number_of_steps+1}, given: {len(CO2_reduction_targets)}.",  # noqa: E501
        )

    return model
