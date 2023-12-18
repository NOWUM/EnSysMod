from tempfile import TemporaryDirectory
from typing import Any, Dict, List, Union
from zipfile import ZipFile

import pandas as pd
from FINE import (
    Conversion,
    EnergySystemModel,
    Sink,
    Source,
    Storage,
    Transmission,
    optimizeSimpleMyopic,
    writeOptimizationOutputToExcel,
)
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import (
    EnergyComponent,
    EnergyConversion,
    EnergyModel,
    EnergyModelOptimization,
    EnergyModelOverride,
    EnergyModelOverrideOperation,
    EnergySink,
    EnergySource,
    EnergyStorage,
    EnergyTransmission,
)
from ensysmod.utils.utils import chdir, create_temp_file


def generate_esm_from_model(db: Session, model: EnergyModel) -> EnergySystemModel:
    """
    Generate an ESM from a given EnergyModel.

    :param db: Database session
    :param model: EnergyModel
    :return: ESM
    """
    regions = model.dataset.regions
    region_ids = [region.id for region in regions]
    commodities = model.dataset.commodities
    esm_data = {
        "hoursPerTimeStep": model.dataset.hours_per_time_step,
        "numberOfTimeSteps": model.dataset.number_of_time_steps,
        "costUnit": model.dataset.cost_unit,
        "lengthUnit": model.dataset.length_unit,
        "locations": set(region.name for region in regions),
        "commodities": set(commodity.name for commodity in commodities),
        "commodityUnitsDict": {commodity.name: commodity.unit for commodity in model.dataset.commodities},
    }

    esM = EnergySystemModel(verboseLogLevel=0, **esm_data)

    # Add all sources
    for source in model.dataset.sources:
        add_source(esM, db, source, region_ids, model.override_parameters)

    # Add all sinks
    for sink in model.dataset.sinks:
        add_sink(esM, db, sink, region_ids, model.override_parameters)

    # Add all conversions
    for conversion in model.dataset.conversions:
        add_conversion(esM, db, conversion, region_ids, model.override_parameters)

    # Add all storages
    for storage in model.dataset.storages:
        add_storage(esM, db, storage, region_ids, model.override_parameters)

    # Add all transmissions
    for transmission in model.dataset.transmissions:
        add_transmission(esM, db, transmission, region_ids, model.override_parameters)

    return esM


def add_source(esM: EnergySystemModel, db: Session, source: EnergySource, region_ids: List[int],
               custom_parameters: List[EnergyModelOverride]) -> None:
    esm_source = component_to_dict(db, source.component, region_ids)
    esm_source["commodity"] = source.commodity.name
    if source.commodity_cost is not None:
        esm_source["commodityCost"] = source.commodity_cost
    if source.yearly_limit is not None:
        esm_source["yearlyLimit"] = -source.yearly_limit  # yearlyLimit for commodity entering the system has to be negative
    if source.commodity_limit_id is not None:
        esm_source["commodityLimitID"] = source.commodity_limit_id
    esm_source = override_parameters(esm_source, custom_parameters)
    esM.add(Source(esM=esM, **esm_source))


def add_sink(esM: EnergySystemModel, db: Session, sink: EnergySink, region_ids: List[int],
             custom_parameters: List[EnergyModelOverride]) -> None:
    esm_sink = component_to_dict(db, sink.component, region_ids)
    esm_sink["commodity"] = sink.commodity.name
    if sink.commodity_cost is not None:
        esm_sink["commodityCost"] = sink.commodity_cost
    if sink.yearly_limit is not None:
        esm_sink["yearlyLimit"] = sink.yearly_limit
    if sink.commodity_limit_id is not None:
        esm_sink["commodityLimitID"] = sink.commodity_limit_id
    esm_sink = override_parameters(esm_sink, custom_parameters)
    esM.add(Sink(esM=esM, **esm_sink))


def add_conversion(esM: EnergySystemModel, db: Session, conversion: EnergyConversion, region_ids: List[int],
                   custom_parameters: List[EnergyModelOverride]) -> None:
    esm_conversion = component_to_dict(db, conversion.component, region_ids)
    esm_conversion["physicalUnit"] = conversion.commodity_unit.unit
    esm_conversion["commodityConversionFactors"] = {x.commodity.name: x.conversion_factor for x in
                                                    conversion.conversion_factors}
    esm_conversion = override_parameters(esm_conversion, custom_parameters)
    esM.add(Conversion(esM=esM, **esm_conversion))


def add_storage(esM: EnergySystemModel, db: Session, storage: EnergyStorage, region_ids: List[int],
                custom_parameters: List[EnergyModelOverride]) -> None:
    esm_storage = component_to_dict(db, storage.component, region_ids)
    esm_storage["commodity"] = storage.commodity.name
    if storage.charge_efficiency is not None:
        esm_storage["chargeEfficiency"] = storage.charge_efficiency
    if storage.discharge_efficiency is not None:
        esm_storage["dischargeEfficiency"] = storage.discharge_efficiency
    if storage.self_discharge is not None:
        esm_storage["selfDischarge"] = storage.self_discharge
    if storage.cyclic_lifetime is not None:
        esm_storage["cyclicLifetime"] = storage.cyclic_lifetime
    if storage.charge_rate is not None:
        esm_storage["chargeRate"] = storage.charge_rate
    if storage.discharge_rate is not None:
        esm_storage["dischargeRate"] = storage.discharge_rate
    if storage.state_of_charge_min is not None:
        esm_storage["stateOfChargeMin"] = storage.state_of_charge_min
    if storage.state_of_charge_max is not None:
        esm_storage["stateOfChargeMax"] = storage.state_of_charge_max
    esm_storage = override_parameters(esm_storage, custom_parameters)
    esM.add(Storage(esM=esM, **esm_storage))


def add_transmission(esM: EnergySystemModel, db: Session, transmission: EnergyTransmission,
                     region_ids: List[int], custom_parameters: List[EnergyModelOverride]) -> None:
    esm_transmission = component_to_dict(db, transmission.component, region_ids)
    esm_transmission["commodity"] = transmission.commodity.name
    component_id = transmission.component.id
    if len(transmission.distances) > 0:
        esm_transmission["distances"] = crud.transmission_distance.get_dataframe(db, component_id=component_id, region_ids=region_ids)
    if len(transmission.losses) > 0:
        esm_transmission["losses"] = crud.transmission_loss.get_dataframe(db, component_id=component_id, region_ids=region_ids)
    esm_transmission = override_parameters(esm_transmission, custom_parameters)
    esM.add(Transmission(esM=esM, **esm_transmission))


def component_to_dict(db: Session, component: EnergyComponent, region_ids: List[int]) -> Dict[str, Any]:
    component_data = {
        "name": component.name,
        "hasCapacityVariable": component.capacity_variable,
        "capacityVariableDomain": component.capacity_variable_domain.value.lower(),
        "capacityPerPlantUnit": component.capacity_per_plant_unit,
        "investPerCapacity": component.invest_per_capacity,
        "opexPerCapacity": component.opex_per_capacity,
        "interestRate": component.interest_rate,
        "economicLifetime": component.economic_lifetime,
        "sharedPotentialID": component.shared_potential_id,
        "linkedQuantityID": component.linked_quantity_id,
    }

    if len(component.capacity_fix) > 0:
        component_data["capacityFix"] = df_or_s(crud.capacity_fix.get_dataframe(db, component_id=component.id, region_ids=region_ids))
    if len(component.capacity_max) > 0:
        component_data["capacityMax"] = df_or_s(crud.capacity_max.get_dataframe(db, component_id=component.id, region_ids=region_ids))
    if len(component.capacity_min) > 0:
        component_data["capacityMin"] = df_or_s(crud.capacity_min.get_dataframe(db, component_id=component.id, region_ids=region_ids))

    if len(component.operation_rate_fix) > 0:
        component_data["operationRateFix"] = df_or_s(crud.operation_rate_fix.get_dataframe(db, component_id=component.id, region_ids=region_ids))
    if len(component.operation_rate_max) > 0:
        component_data["operationRateMax"] = df_or_s(crud.operation_rate_max.get_dataframe(db, component_id=component.id, region_ids=region_ids))

    if len(component.yearly_full_load_hours_max) > 0:
        component_data["yearlyFullLoadHoursMax"] = df_or_s(crud.yearly_full_load_hours_max.get_dataframe(db, component_id=component.id, region_ids=region_ids))
    if len(component.yearly_full_load_hours_min) > 0:
        component_data["yearlyFullLoadHoursMin"] = df_or_s(crud.yearly_full_load_hours_min.get_dataframe(db, component_id=component.id, region_ids=region_ids))

    return component_data


def override_parameters(component_dict: Dict, custom_parameters: List[EnergyModelOverride]) -> Dict:
    """
    Overrides component parameters.
    """
    for custom_parameter in custom_parameters:
        if custom_parameter.component.name != component_dict["name"]:
            continue

        attribute_name = custom_parameter.attribute.name
        if attribute_name not in component_dict.keys():
            raise ValueError(f"Parameter {attribute_name} is undefined for component {component_dict['name']}.")

        if custom_parameter.operation == EnergyModelOverrideOperation.add:
            component_dict[attribute_name] += custom_parameter.value
        elif custom_parameter.operation == EnergyModelOverrideOperation.multiply:
            component_dict[attribute_name] *= custom_parameter.value
        elif custom_parameter.operation == EnergyModelOverrideOperation.set:
            component_dict[attribute_name] = custom_parameter.value
        else:
            raise ValueError(f"Unknown operation: {custom_parameter.operation}")
    return component_dict


def optimize_esm(esM: EnergySystemModel):
    """
    Optimize the energy system model.
    """
    esM.cluster(numberOfTypicalPeriods=7)
    esM.optimize(timeSeriesAggregation=True)

    result_file_path = create_temp_file(prefix="ensysmod_result_", suffix=".xlsx")
    base_name = str(result_file_path.with_suffix(""))
    writeOptimizationOutputToExcel(esM=esM, outputFileName=base_name, optSumOutputLevel=2, optValOutputLevel=1)
    return result_file_path


def myopic_optimize_esm(esM: EnergySystemModel, optimization_parameters: EnergyModelOptimization):
    """
    Optimization function for myopic approach. For each optimization run, the newly installed capacities
    will be given as a stock (with capacityFix) to the next optimization run.
    """
    start_year = optimization_parameters.start_year
    end_year = optimization_parameters.end_year
    nb_of_steps = optimization_parameters.number_of_steps
    nb_of_represented_years = optimization_parameters.years_per_step
    CO2_reference = optimization_parameters.CO2_reference
    CO2_reduction_targets = optimization_parameters.CO2_reduction_targets

    if CO2_reduction_targets is not None:
        check_CO2_optimization_sink(esM)

    with TemporaryDirectory(prefix="ensysmod_") as temp_dir, chdir(temp_dir):
        # optimizeSimpleMyopic() can only output files to the current working directory
        optimizeSimpleMyopic(
            esM=esM,
            startYear=start_year,
            endYear=end_year,
            nbOfSteps=nb_of_steps,
            nbOfRepresentedYears=nb_of_represented_years,
            CO2Reference=CO2_reference,
            CO2ReductionTargets=CO2_reduction_targets,
            trackESMs=False,
        )
        result_excel_files = [f"ESM{year}.xlsx" for year in range(start_year, end_year+1, nb_of_represented_years)]
        zipped_result_file_path = create_temp_file(prefix="ensysmod_result_", suffix=".zip")
        with ZipFile(zipped_result_file_path, "w") as zip_file:
            for file in result_excel_files:
                zip_file.write(file)

    return zipped_result_file_path


def check_CO2_optimization_sink(esM: EnergySystemModel):
    """
    Checks the required Sink component for the CO2 optimization to function properly.
    """
    if ('CO2 to environment', 'SourceSinkModel') not in esM.componentNames.items():
        raise ValueError("Sink component with the name 'CO2 to environment' is required.")

    if esM.getComponentAttribute(componentName='CO2 to environment', attributeName='commodityLimitID') is None:
        raise ValueError("Commodity limit ID of the sink component 'CO2 to environment' must be specified.")


def df_or_s(dataframe: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
    if dataframe.shape[0] == 1:
        return dataframe.squeeze(axis=0)
    else:
        return dataframe
