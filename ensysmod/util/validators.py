from typing import Any, List

from ensysmod.model import EnergyComponentType
# from ensysmod.schemas.energy_conversion_factor import EnergyConversionFactorCreate
# from ensysmod.schemas.energy_transmission import EnergyTransmissionCreate


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


def validate_ref_dataset(ref_dataset: int) -> int:
    """
    Validates the referenz to a dataset of an object.

    :param ref_dataset: The referenz to a dataset of the object.
    :return: The validated referenz to a dataset.
    """
    if not ref_dataset:
        raise ValueError("Referenz to a dataset must not be empty.")
    if ref_dataset <= 0:
        raise ValueError("Referenz to a dataset must be positiv.")

    return ref_dataset


def validate_capacity_per_plant_unit(capacity_per_plant_unit: float) -> float:
    """
    Validates the capacity per plant per unit of an object.

    :param capacity_per_plant_unit: The capacity per plant per unit of the object.
    :return: The validated capacity per plant per unit.
    """
    if capacity_per_plant_unit is None:
        # Skip validation if no value provided
        return None
    if capacity_per_plant_unit <= 0:
        raise ValueError("Capacity per plant per unit must be positiv.")

    return capacity_per_plant_unit


def validate_invest_per_capacity(invest_per_capacity: float) -> float:
    """
    Validates the invest per capacity of an object.

    :param invest_per_capacity: The invest per capacity of the object.
    :return: The validated invest per capacity.
    """
    if invest_per_capacity is None:
        # Skip validation if no value provided
        return None
    if invest_per_capacity and invest_per_capacity < 0:
        raise ValueError("Invest per capacity must be zero or positiv.")

    return invest_per_capacity


def validate_opex_per_capacity(opex_per_capacity: float) -> float:
    """
    Validates the opex per capacity of an object.

    :param opex_per_capacity: The opex per capacity of the object.
    :return: The validated opex per capacity.
    """
    if opex_per_capacity is None:
        # Skip validation if no value provided
        return None
    if opex_per_capacity < 0:
        raise ValueError("Opex per capacity must be zero or positiv.")

    return opex_per_capacity


def validate_interest_rate(interest_rate: float) -> float:
    """
    Validates the interest rate of an object.

    :param interest_rate: The interest rate of the object.
    :return: The validated interest rate.
    """
    if interest_rate is None:
        # Skip validation if no value provided
        return None
    if (interest_rate < 0 or interest_rate > 1):
        raise ValueError("Interest rate must be between 0 and 1.")

    return interest_rate


def validate_economic_lifetime(economic_lifetime: int) -> int:
    """
    Validates the economic lifetime of an object.

    :param economic_lifetime: The economic lifetime of the object.
    :return: The validated economic lifetime.
    """
    if economic_lifetime is None:
        # Skip validation if no value provided
        return None
    if economic_lifetime <= 0:
        raise ValueError("Economic lifetime must be positiv.")

    return economic_lifetime


def validate_shared_potential_id(shared_potential_id: str) -> str:
    """
    Validates the shared potential id of an object.

    :param shared_potential_id: The shared potential id of the object.
    :return: The validated shared potential id.
    """
    if shared_potential_id is None:
        # Skip validation if no value provided
        return None
    if len(shared_potential_id) > 100:
        raise ValueError("Shared potential id must not be longer than 100 characters.")
    return shared_potential_id


def validate_conversion_factor(conversion_factor: float) -> float:
    """
    Validates the conversion factor of an object.

    :param conversion_factor: The conversion factor of the object.
    :return: The validated conversion factor.
    """
    if conversion_factor is None:
        # Skip validation if no value provided
        return None
    if (conversion_factor < 0 or conversion_factor > 1):
        raise ValueError("Conversion factor must be between 0 and 1.")

    return conversion_factor


def validate_commodity(commodity: str) -> str:
    """
    Validates the commodity of an object.

    :param commodity: The commodity of the object.
    :return: The validated commodity.
    """
    if commodity is None:
        # Skip validation if no value provided
        return None
    if len(commodity) > 100:
        raise ValueError("commodity must not be longer than 100 characters.")
    return commodity


def validate_ref_component(ref_component: int) -> int:
    """
    Validates the referenz to a component of an object.

    :param ref_component: The referenz to a component of the object.
    :return: The validated referenz to a component.
    """
    if ref_component <= 0:
        raise ValueError("Referenz to a component must be positiv.")

    return ref_component


def validate_conversion_factors(conversion_factors: List[Any]) -> List[Any]:
    """
    Validates the conversion_factor of an object.

    :param conversion_factor: The conversion_factor of the object.
    :return: The validated conversion_factor.
    """
    if not conversion_factors:
        raise ValueError("List must not be empty.")

    return conversion_factors


def validate_yearly_co2_limit(yearly_co2_limit: float) -> float:
    """
    Validates the yearly_co2_limit of an object.

    :param yearly_co2_limit: The yearly_co2_limit of the object.
    :return: The validated yearly_co2_limit.
    """
    if yearly_co2_limit <= 0:
        raise ValueError("yearly_co2_limit must be positiv.")

    return yearly_co2_limit


def validate_commodity_cost(commodity_cost: float) -> float:
    """
    Validates the commodity_cost of an object.

    :param commodity_cost: The commodity_cost of the object.
    :return: The validated commodity_cost.
    """
    if commodity_cost < 0:
        raise ValueError("commodity_cost must be zero or positiv.")

    return commodity_cost


def validate_charge_efficiency(charge_efficiency: float) -> float:
    """
    Validates the charge_efficiency of an object.

    :param charge_efficiency: The charge_efficiency of the object.
    :return: The validated charge_efficiency.
    """
    if (charge_efficiency < 0 or charge_efficiency > 1):
        raise ValueError("charge_efficiency must be between 0 and 1.")

    return charge_efficiency


def validate_discharge_efficiency(discharge_efficiency: float) -> float:
    """
    Validates the discharge_efficiency of an object.

    :param discharge_efficiency: The discharge_efficiency of the object.
    :return: The validated discharge_efficiency.
    """
    if (discharge_efficiency < 0 or discharge_efficiency > 1):
        raise ValueError("discharge_efficiency must be between 0 and 1.")

    return discharge_efficiency


def validate_self_discharge(self_discharge: float) -> float:
    """
    Validates the self_discharge of an object.

    :param self_discharge: The self_discharge of the object.
    :return: The validated self_discharge.
    """
    if (self_discharge < 0 or self_discharge > 1):
        raise ValueError("self_discharge must be between 0 and 1.")

    return self_discharge


def validate_cyclic_lifetime(cyclic_lifetime: int) -> int:
    """
    Validates the cyclic_lifetime of an object.

    :param cyclic_lifetime: The cyclic_lifetime of the object.
    :return: The validated cyclic_lifetime.
    """
    if cyclic_lifetime <= 0:
        raise ValueError("self_discharge must be positive.")

    return cyclic_lifetime


def validate_charge_rate(charge_rate: float) -> float:
    """
    Validates the charge_rate of an object.

    :param charge_rate: The charge_rate of the object.
    :return: The validated charge_rate.
    """
    if (charge_rate < 0 or charge_rate > 1):
        raise ValueError("charge_rate must be between 0 and 1.")

    return charge_rate


def validate_discharge_rate(discharge_rate: float) -> float:
    """
    Validates the discharge_rate of an object.

    :param discharge_rate: The discharge_rate of the object.
    :return: The validated discharge_rate.
    """
    if (discharge_rate < 0 or discharge_rate > 1):
        raise ValueError("discharge_rate must be between 0 and 1.")

    return discharge_rate


def validate_state_of_charge_min(state_of_charge_min: float) -> float:
    """
    Validates the state_of_charge_min of an object.

    :param state_of_charge_min: The state_of_charge_min of the object.
    :return: The validated state_of_charge_min.
    """
    if (state_of_charge_min < 0 or state_of_charge_min > 1):
        raise ValueError("state_of_charge_min must be between 0 and 1.")

    return state_of_charge_min


def validate_state_of_charge_max(state_of_charge_max: float) -> float:
    """
    Validates the state_of_charge_max of an object.

    :param state_of_charge_max: The state_of_charge_max of the object.
    :return: The validated state_of_charge_max.
    """
    if (state_of_charge_max < 0 or state_of_charge_max > 1):
        raise ValueError("state_of_charge_max must be between 0 and 1.")

    return state_of_charge_max


def validate_distance(distance: float) -> float:
    """
    Validates the distance of an object.

    :param distance: The distance of the object.
    :return: The validated distance.
    """
    if distance < 0:
        raise ValueError("distance must be zero or positive.")

    return distance


def validate_component(component: str) -> str:
    """
    Validates the component of an object.

    :param component: The component of the object.
    :return: The validated component.
    """
    if len(component) > 100:
        raise ValueError("component must not be longer than 100 characters.")

    return component


def validate_region_from(region_from: str) -> str:
    """
    Validates the region_from of an object.

    :param region_from: The region_from of the object.
    :return: The validated region_from.
    """
    if len(region_from) > 100:
        raise ValueError("region_from must not be longer than 100 characters.")

    return region_from


def validate_region_to(region_to: str) -> str:
    """
    Validates the region_to of an object.

    :param region_to: The region_to of the object.
    :return: The validated region_to.
    """
    if len(region_to) > 100:
        raise ValueError("region_to must not be longer than 100 characters.")

    return region_to


def validate_ref_region_from(ref_region_from: int) -> int:
    """
    Validates the ref_region_from of an object.

    :param ref_region_from: The ref_region_from of the object.
    :return: The validated ref_region_from.
    """
    if ref_region_from <= 0:
        raise ValueError("ref_region_from must be positiv.")

    return ref_region_from


def validate_ref_region_to(ref_region_to: int) -> int:
    """
    Validates the ref_region_to of an object.

    :param ref_region_to: The ref_region_to of the object.
    :return: The validated ref_region_to.
    """
    if ref_region_to <= 0:
        raise ValueError("ref_region_to must be positiv.")

    return ref_region_to


def validate_loss_per_unit(loss_per_unit: float) -> float:
    """
    Validates the loss_per_unit of an object.

    :param loss_per_unit: The loss_per_unit of the object.
    :return: The validated loss_per_unit.
    """
    if (loss_per_unit < 0 or loss_per_unit > 1):
        raise ValueError("loss_per_unit must be zero or positive.")

    return loss_per_unit


def validate_distances(distances: List[Any]) -> List[Any]:
    """
    Validates the distances of an object.

    :param distances: The distances of the object.
    :return: The validated distances.
    """
    if not distances:
        raise ValueError("List must not be empty.")

    return distances


def validate_fix_capacities(fix_capacities: List[float]) -> List[float]:
    """
    Validates the fix_capacities of an object.

    :param fix_capacities: The fix_capacities of the object.
    :return: The validated fix_capacities.
    """
    if not fix_capacities:
        raise ValueError("List must not be empty.")

    return fix_capacities


def validate_max_capacities(max_capacities: List[float]) -> List[float]:
    """
    Validates the max_capacities of an object.

    :param max_capacities: The max_capacities of the object.
    :return: The validated max_capacities.
    """
    if not max_capacities:
        raise ValueError("List must not be empty.")

    return max_capacities


def validate_fix_operation_rates(fix_operation_rates: List[float]) -> List[float]:
    """
    Validates the fix_operation_rates of an object.

    :param fix_operation_rates: The fix_operation_rates of the object.
    :return: The validated fix_operation_rates.
    """
    if not fix_operation_rates:
        raise ValueError("List must not be empty.")

    return fix_operation_rates


def validate_max_operation_rates(max_operation_rates: List[float]) -> List[float]:
    """
    Validates the max_operation_rates of an object.

    :param max_operation_rates: The max_operation_rates of the object.
    :return: The validated max_operation_rates.
    """
    if not max_operation_rates:
        raise ValueError("List must not be empty.")

    return max_operation_rates
