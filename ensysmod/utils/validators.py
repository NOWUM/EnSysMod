from typing import Any, List, Optional

from pydantic.errors import MissingError

from ensysmod.model import EnergyComponentType


def validate_name(name: str) -> str:
    """
    Validates the name of an object.

    :param name: The name of the object.
    :return: The validated name.
    """
    if not name:
        raise ValueError("Name must not be empty.")
    if len(name) > 255:
        raise ValueError("Name must not be longer than 255 characters.")
    return name


def validate_description(description: str) -> str:
    """
    Validates the description of an object.

    :param description: The description of the object.
    :return: The validated description.
    """
    if description and len(description) > 1024:
        raise ValueError("Description must not be longer than 1024 characters.")
    return description


def validate_energy_component_type(energy_component_type: EnergyComponentType) -> EnergyComponentType:
    """
    Validates the energy component type of an object.

    :param energy_component_type: The energy component type of the object.
    :return: The validated energy component type.
    """
    if energy_component_type == EnergyComponentType.UNDEFINED:
        raise ValueError("Energy component type must not be undefined.")
    return energy_component_type


def validate_unit(unit: str) -> str:
    """
    Validates the unit of an object.

    :param unit: The unit of the object.
    :return: The validated unit.
    """
    if not unit:
        raise ValueError("Unit must not be empty.")
    if len(unit) > 100:
        raise ValueError("Unit must not be longer than 100 characters.")
    return unit


def validate_ref_dataset_required(ref_dataset: int) -> int:
    """
    Validates the reference to a dataset of an object.

    :param ref_dataset: The reference to a dataset of the object.
    :return: The validated reference to a dataset.
    """
    if ref_dataset is None:
        raise ValueError("Reference to a dataset must not be empty.")

    if ref_dataset <= 0:
        raise ValueError("Reference to a dataset must be positive.")

    return ref_dataset


def validate_ref_dataset_optional(ref_dataset: Optional[int]) -> Optional[int]:
    """
    Validates the reference to a dataset of an object.

    :param ref_dataset: The reference to a dataset of the object.
    :return: The validated reference to a dataset.
    """
    if ref_dataset is None:
        return None
    if ref_dataset <= 0:
        raise ValueError("Reference to a dataset must be positive.")

    return ref_dataset


def validate_capacity_per_plant_unit(capacity_per_plant_unit: Optional[float]) -> Optional[float]:
    """
    Validates the capacity per plant per unit of an object.
    Capacity per plant per unit is always optional.

    :param capacity_per_plant_unit: The capacity per plant per unit of the object.
    :return: The validated capacity per plant per unit.
    """
    if capacity_per_plant_unit is None:
        # Skip validation if no value provided
        return None

    if capacity_per_plant_unit <= 0:
        raise ValueError("Capacity per plant per unit must be positive.")

    return capacity_per_plant_unit


def validate_invest_per_capacity(invest_per_capacity: Optional[float]) -> Optional[float]:
    """
    Validates the invest per capacity of an object.
    Invest per capacity is always optional.

    :param invest_per_capacity: The invest per capacity of the object.
    :return: The validated invest per capacity.
    """
    if invest_per_capacity is None:
        # Skip validation if no value provided
        return None

    if invest_per_capacity < 0:
        raise ValueError("Invest per capacity must be zero or positive.")

    return invest_per_capacity


def validate_opex_per_capacity(opex_per_capacity: Optional[float]) -> Optional[float]:
    """
    Validates the opex per capacity of an object.
    Opex per capacity is always optional.

    :param opex_per_capacity: The opex per capacity of the object.
    :return: The validated opex per capacity.
    """
    if opex_per_capacity is None:
        # Skip validation if no value provided
        return None

    if opex_per_capacity < 0:
        raise ValueError("Opex per capacity must be zero or positive.")

    return opex_per_capacity


def validate_interest_rate(interest_rate: Optional[float]) -> Optional[float]:
    """
    Validates the interest rate of an object.
    Interest rate is always optional.

    :param interest_rate: The interest rate of the object.
    :return: The validated interest rate.
    """
    if interest_rate is None:
        # Skip validation if no value provided
        return None

    if interest_rate < 0 or interest_rate > 1:
        raise ValueError("Interest rate must be between 0 and 1.")

    return interest_rate


def validate_economic_lifetime(economic_lifetime: Optional[int]) -> Optional[int]:
    """
    Validates the economic lifetime of an object.
    Economic lifetime is always optional.

    :param economic_lifetime: The economic lifetime of the object.
    :return: The validated economic lifetime.
    """
    if economic_lifetime is None:
        # Skip validation if no value provided
        return None

    if economic_lifetime <= 0:
        raise ValueError("Economic lifetime must be positive.")

    return economic_lifetime


def validate_shared_potential_id(shared_potential_id: Optional[str]) -> Optional[str]:
    """
    Validates the shared potential id of an object.
    Shared potential id is always optional.

    :param shared_potential_id: The shared potential id of the object.
    :return: The validated shared potential id.
    """
    if shared_potential_id is None:
        # Skip validation if no value provided
        return None

    if len(shared_potential_id) > 100:
        raise ValueError("Shared potential id must not be longer than 100 characters.")

    return shared_potential_id


def validate_linked_quantity_id(linked_quantity_id: Optional[str]) -> Optional[str]:
    """
    Validates the linked quantity id of an object.
    Linked quantity id is always optional.

    :param linked_quantity_id: The linked quantity id of the object.
    :return: The validated linked quantity id.
    """
    if linked_quantity_id is None:
        # Skip validation if no value provided
        return None

    if len(linked_quantity_id) > 100:
        raise ValueError("Linked quantity id must not be longer than 100 characters.")

    return linked_quantity_id


def validate_conversion_factor(conversion_factor: Optional[float]) -> Optional[float]:
    """
    Validates the conversion factor of an object.
    Conversion factor is always optional.

    :param conversion_factor: The conversion factor of the object.
    :return: The validated conversion factor.
    """
    if conversion_factor is None:
        # Skip validation if no value provided
        return None
    if conversion_factor < -5 or conversion_factor > 5:
        raise ValueError("Conversion factor must be between -5 and 5.")

    return conversion_factor


def validate_commodity(commodity: Optional[str]) -> Optional[str]:
    """
    Validates the commodity of an object.

    :param commodity: The commodity of the object.
    :return: The validated commodity.
    """
    if commodity is None:
        # Skip validation if no value provided
        return None
    if not commodity:
        raise ValueError("Commodity must not be empty.")
    if len(commodity) > 255:
        raise ValueError("Commodity must not be longer than 255 characters.")

    return commodity


def validate_ref_component_required(ref_component: int) -> int:
    """
    Validates the reference to a component of an object.

    :param ref_component: The reference to a component of the object.
    :return: The validated reference to a component.
    """
    if ref_component <= 0:
        raise ValueError("Reference to a component must be positive.")

    return ref_component


def validate_ref_component_optional(ref_component: Optional[int]) -> Optional[int]:
    """
    Validates the reference to a component of an object.

    :param ref_component: The reference to a component of the object.
    :return: The validated reference to a component.
    """
    if ref_component is None:
        return None

    if ref_component <= 0:
        raise ValueError("Reference to a component must be positive.")

    return ref_component


def validate_conversion_factors(conversion_factors: List[Any]) -> List[Any]:
    """
    Validates the conversion factors of an object.

    :param conversion_factors: The conversion_factor of the object.
    :return: The validated conversion_factor.
    """
    if conversion_factors is None:
        raise MissingError()
    if len(conversion_factors) == 0:
        raise ValueError("List of conversion factors must not be empty.")

    return conversion_factors


def validate_commodity_cost(commodity_cost: float) -> Optional[float]:
    """
    Validates the commodity cost of an object.

    :param commodity_cost: The commodity cost of the object.
    :return: The validated commodity cost.
    """
    if commodity_cost is None:
        return None
    if commodity_cost < 0:
        raise ValueError("Commodity cost must be zero or positive.")

    return commodity_cost


def validate_yearly_limit_and_commodity_limit_id(cls, values):
    """
    Validates the yearly limit and the commodity limit ID of an object.

    :param yearly_limit: The yearly limit of the object.
    :param commodity_limit_id: The commodity limit id of the object.
    :return: The validated yearly limit and commodity limit id.
    """
    yearly_limit, commodity_limit_id = values.get('yearly_limit'), values.get('commodity_limit_id')

    if yearly_limit is None and commodity_limit_id is None:
        # Skip validation if no value provided
        return values
    if yearly_limit is not None and commodity_limit_id is None:
        raise ValueError("If yearly_limit is specified, commodity_limit_id must be specified as well.")

    if yearly_limit < 0:
        raise ValueError("Yearly limit must be zero or positive.")
    if len(commodity_limit_id) > 100:
        raise ValueError("Commodity limit ID must not be longer than 100 characters.")

    return values


def validate_charge_efficiency(charge_efficiency: Optional[float]) -> Optional[float]:
    """
    Validates the charge efficiency of an object.
    Charge efficiency is always optional.

    :param charge_efficiency: The charge efficiency of the object.
    :return: The validated charge efficiency.
    """
    if charge_efficiency is None:
        return None

    if charge_efficiency < 0 or charge_efficiency > 1:
        raise ValueError("Charge efficiency must be between 0 and 1.")

    return charge_efficiency


def validate_discharge_efficiency(discharge_efficiency: Optional[float]) -> Optional[float]:
    """
    Validates the discharge efficiency of an object.
    Discharge efficiency is always optional.

    :param discharge_efficiency: The discharge efficiency of the object.
    :return: The validated discharge efficiency.
    """
    if discharge_efficiency is None:
        return None

    if discharge_efficiency < 0 or discharge_efficiency > 1:
        raise ValueError("Discharge efficiency must be between 0 and 1.")

    return discharge_efficiency


def validate_self_discharge(self_discharge: Optional[float]) -> Optional[float]:
    """
    Validates the self discharge of an object.
    Self discharge is always optional.

    :param self_discharge: The self discharge of the object.
    :return: The validated self discharge.
    """
    if self_discharge is None:
        return None

    if self_discharge < 0 or self_discharge > 1:
        raise ValueError("Self discharge must be between 0 and 1.")

    return self_discharge


def validate_cyclic_lifetime(cyclic_lifetime: Optional[int]) -> Optional[int]:
    """
    Validates the cyclic lifetime of an object.
    Cyclic lifetime is always optional.

    :param cyclic_lifetime: The cyclic_lifetime of the object.
    :return: The validated cyclic lifetime.
    """
    if cyclic_lifetime is None:
        return None

    if cyclic_lifetime <= 0:
        raise ValueError("Cyclic lifetime must be positive.")

    return cyclic_lifetime


def validate_charge_rate(charge_rate: Optional[float]) -> Optional[float]:
    """
    Validates the charge rate of an object.
    Charge rate is always optional.

    :param charge_rate: The charge rate of the object.
    :return: The validated charge rate.
    """
    if charge_rate is None:
        return None

    if charge_rate < 0 or charge_rate > 1:
        raise ValueError("Charge rate must be between 0 and 1.")

    return charge_rate


def validate_discharge_rate(discharge_rate: Optional[float]) -> Optional[float]:
    """
    Validates the discharge rate of an object.
    Discharge rate is always optional.

    :param discharge_rate: The discharge rate of the object.
    :return: The validated discharge rate.
    """
    if discharge_rate is None:
        return None

    if discharge_rate < 0 or discharge_rate > 1:
        raise ValueError("Discharge rate must be between 0 and 1.")

    return discharge_rate


def validate_state_of_charge_min(state_of_charge_min: Optional[float]) -> Optional[float]:
    """
    Validates the state of charge min of an object.
    State of charge min is always optional.

    :param state_of_charge_min: The state of charge min of the object.
    :return: The validated state of charge min.
    """
    if state_of_charge_min is None:
        return None

    if state_of_charge_min < 0 or state_of_charge_min > 1:
        raise ValueError("State of charge min must be between 0 and 1.")

    return state_of_charge_min


def validate_state_of_charge_max(state_of_charge_max: Optional[float]) -> Optional[float]:
    """
    Validates the state of charge max of an object.
    State of charge max is always optional.

    :param state_of_charge_max: The state of charge max of the object.
    :return: The validated state of charge max.
    """
    if state_of_charge_max is None:
        return None
    if state_of_charge_max < 0 or state_of_charge_max > 1:
        raise ValueError("State of charge max must be between 0 and 1.")

    return state_of_charge_max


def validate_distance(distance: float) -> float:
    """
    Validates the distance of an object.

    :param distance: The distance of the object.
    :return: The validated distance.
    """
    if distance < 0:
        raise ValueError("The distance must be zero or positive.")

    return distance


def validate_loss(loss: float) -> float:
    """
    Validates the loss of an object.

    :param loss: The loss of the object.
    :return: The validated loss.
    """
    if loss < 0 or loss > 1:
        raise ValueError("The loss must be between zero and one.")

    return loss


def validate_fix_capacities(fix_capacities: List[float]) -> List[float]:
    """
    Validates the fix capacities of an object.

    :param fix_capacities: The fix capacities of the object.
    :return: The validated fix capacities.
    """
    if not fix_capacities:
        raise ValueError("List of fix capacities must not be empty.")

    return fix_capacities


def validate_max_capacities(max_capacities: List[float]) -> List[float]:
    """
    Validates the max capacities of an object.

    :param max_capacities: The max capacities of the object.
    :return: The validated max capacities.
    """
    if not max_capacities:
        raise ValueError("List of max capacities must not be empty.")

    return max_capacities


def validate_min_capacities(min_capacities: List[float]) -> List[float]:
    """
    Validates the min capacities of an object.

    :param min_capacities: The min capacities of the object.
    :return: The validated min capacities.
    """
    if not min_capacities:
        raise ValueError("List of min capacities must not be empty.")

    return min_capacities


def validate_fix_operation_rates(fix_operation_rates: List[float]) -> List[float]:
    """
    Validates the fix operation rates of an object.

    :param fix_operation_rates: The fix operation rates of the object.
    :return: The validated fix operation rates.
    """
    if not fix_operation_rates:
        raise ValueError("List of fix operation rates must not be empty.")

    return fix_operation_rates


def validate_max_operation_rates(max_operation_rates: List[float]) -> List[float]:
    """
    Validates the max operation rates of an object.

    :param max_operation_rates: The max operation rates of the object.
    :return: The validated max operation rates.
    """
    if not max_operation_rates:
        raise ValueError("List of max operation rates must not be empty.")

    return max_operation_rates


def validate_optimization_timeframe(cls, values):
    """
    Validates the optimization timeframe of an object.

    :param start_year: Year of the first optimization.
    :param end_year: Year of the last optimization.
    :param number_of_steps: Number of optimization runs excluding the start year.
    :param years_per_step: Number of years represented by one optimization run.

    :return: the validated optimization timeframe parameters.
    """
    start_year = values.get('start_year')
    end_year = values.get('end_year')
    number_of_steps = values.get('number_of_steps')
    years_per_step = values.get('years_per_step')

    if start_year is None:
        raise ValueError("start_year must be specified.")
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
        number_of_steps = (end_year - start_year)/years_per_step
    elif (end_year is not None) & (number_of_steps is not None) & (years_per_step is None):
        years_per_step = (end_year - start_year)/number_of_steps

    if (end_year - start_year) != number_of_steps * years_per_step:
        raise ValueError("The parameters must satisfy the equation: (end_year - start_year) = number_of_steps * years_per_step.")

    values['start_year'] = start_year
    values['end_year'] = end_year
    values['number_of_steps'] = number_of_steps
    values['years_per_step'] = years_per_step

    return values


def validate_CO2_optimization(cls, values):
    """
    Validates the CO2 optimization.

    :param CO2_reference: CO2 emission reference value to which the reduction should be applied to.
    :param CO2_reduction_targets: CO2 reduction targets for all optimization periods, in percentages. If specified, the length of the list must equal the number of optimization steps.

    :return: The validated CO2 optimization parameters.
    """  # noqa: E501
    CO2_reference = values.get('CO2_reference')
    CO2_reduction_targets = values.get('CO2_reduction_targets')
    number_of_steps = values.get('number_of_steps')

    if (CO2_reference is None) & (CO2_reduction_targets is None):
        return values
    if (CO2_reference is not None) & (CO2_reduction_targets is None):
        raise ValueError("If CO2_reference is specified, CO2_reduction_targets must also be specified.")
    if (CO2_reference is None) & (CO2_reduction_targets is not None):
        raise ValueError("If CO2_reduction_targets is specified, CO2_reference must also be specified.")

    if CO2_reference < 0:
        raise ValueError("CO2_reference must be zero or positive.")
    for target in CO2_reduction_targets:
        if target < 0 or target > 100:
            raise ValueError("Values of CO2_reduction_targets must be between 0 and 100.")

    if len(CO2_reduction_targets) != number_of_steps+1:
        raise ValueError(
            f"The number of values given in CO2_reduction_targets must match the number of optimization runs. Expected: {number_of_steps+1}, given: {len(CO2_reduction_targets)}."  # noqa: E501
        )

    return values
