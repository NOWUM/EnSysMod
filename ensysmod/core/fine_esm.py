from datetime import datetime
from typing import Any, Dict, List, Union

import pandas as pd
from FINE import EnergySystemModel, Storage, Sink, Transmission, Conversion, Source, writeOptimizationOutputToExcel
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyModel, EnergyComponent


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
        # "hoursPerTimeStep": model.dataset.hours_per_time_step,
        # "numberOfTimeSteps": model.dataset.number_of_time_steps,
        # "costUnit": model.dataset.cost_unit,
        # "lengthUnit": model.dataset.length_unit,
        "locations": set(region.name for region in regions),
        "commodities": set(commodity.name for commodity in commodities),
        "commodityUnitsDict": {commodity.name: commodity.unit for commodity in model.dataset.commodities},
    }

    esM = EnergySystemModel(verboseLogLevel=0, **esm_data)

    # Add all sources
    for source in model.dataset.sources:
        esm_source = component_to_dict(db, source.component, region_ids)
        esm_source["commodity"] = source.commodity.name
        if source.commodity_cost is not None:
            esm_source["commodityCost"] = source.commodity_cost
        esM.add(Source(esM=esM, **esm_source))

    # Add all sinks
    for sink in model.dataset.sinks:
        esm_sink = component_to_dict(db, sink.component, region_ids)
        esm_sink["commodity"] = sink.commodity.name
        esM.add(Sink(esM=esM, **esm_sink))

    # Add all conversions
    for conversion in model.dataset.conversions:
        esm_conversion = component_to_dict(db, conversion.component, region_ids)
        esm_conversion["physicalUnit"] = conversion.commodity_unit.unit
        esm_conversion["commodityConversionFactors"] = {x.commodity.name: x.conversion_factor for x in
                                                        conversion.conversion_factors}
        esM.add(Conversion(esM=esM, **esm_conversion))

    # Add all storages
    for storage in model.dataset.storages:
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
        esM.add(Storage(esM=esM, **esm_storage))

    # Add all transmissions
    for transmission in model.dataset.transmissions:
        esm_transmission = component_to_dict(db, transmission.component, region_ids)
        esm_transmission["commodity"] = transmission.commodity.name
        esm_transmission["distances"] = crud.energy_transmission_distance.get_dataframe(db, transmission.ref_component,
                                                                                        region_ids=region_ids)
        esM.add(Transmission(esM=esM, **esm_transmission))

    return esM


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
    }
    if component.shared_potential_id is not None:
        component_data["sharedPotentialID"] = component.shared_potential_id

    if crud.capacity_max.has_data(db, component_id=component.id, region_ids=region_ids):
        component_data["capacityMax"] = df_or_s(crud.capacity_max.get_dataframe(db, component_id=component.id,
                                                                                region_ids=region_ids))

    if crud.capacity_fix.has_data(db, component_id=component.id, region_ids=region_ids):
        component_data["capacityFix"] = df_or_s(crud.capacity_fix.get_dataframe(db, component_id=component.id,
                                                                                region_ids=region_ids))

    if crud.operation_rate_max.has_data(db, component_id=component.id, region_ids=region_ids):
        component_data["operationRateMax"] = df_or_s(crud.operation_rate_max.get_dataframe(db,
                                                                                           component_id=component.id,
                                                                                           region_ids=region_ids))

    if crud.operation_rate_fix.has_data(db, component_id=component.id, region_ids=region_ids):
        component_data["operationRateFix"] = df_or_s(crud.operation_rate_fix.get_dataframe(db,
                                                                                           component_id=component.id,
                                                                                           region_ids=region_ids))

    return component_data


def optimize_esm(esM: EnergySystemModel):
    """
    Optimize the energy system model.
    """
    esM.cluster(numberOfTypicalPeriods=7)
    esM.optimize(timeSeriesAggregation=True, optimizationSpecs='OptimalityTol=1e-3 method=2 cuts=0', solver='gurobi')

    time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    result_file_path = f"./tmp/result-{time_str}"
    writeOptimizationOutputToExcel(esM=esM,
                                   outputFileName=result_file_path,
                                   optSumOutputLevel=2, optValOutputLevel=1)
    return result_file_path + ".xlsx"


def df_or_s(dataframe: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
    if dataframe.shape[0] == 1:
        return dataframe.squeeze(axis=0)
    else:
        return dataframe
