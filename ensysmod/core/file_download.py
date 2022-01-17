import os
import zipfile
from typing import Any, Type, Set, Dict, List

import simplejson as json
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ensysmod import crud, schemas
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.utils import jsonable_encoder


def export_data(db: Session, dataset_id: int, temp_folder: str) -> str:
    """
    Create a zip file for the dataset.

    :param db: database session
    :param dataset_id: dataset id
    :param temp_folder: temporary folder
    :return: Path to zip file
    """

    # create commodities.json
    dump_json(f"{temp_folder}/commodities.json", set(schemas.EnergyCommodityCreate.__fields__.keys()),
              crud.energy_commodity.get_multi_by_dataset(db, dataset_id=dataset_id))

    # create regions.json
    regions = crud.region.get_multi_by_dataset(db, dataset_id=dataset_id)
    dump_json(f"{temp_folder}/regions.json", set(schemas.RegionCreate.__fields__.keys()),
              regions)

    region_ids = [region.id for region in regions]
    dump_energy_components(db, dataset_id, temp_folder + "conversions/", crud.energy_conversion,
                           "conversion", schemas.EnergyConversionCreate, region_ids)

    dump_energy_components(db, dataset_id, temp_folder + "sources/", crud.energy_source,
                           "source", schemas.EnergySourceCreate, region_ids)

    dump_energy_components(db, dataset_id, temp_folder + "sinks/", crud.energy_sink,
                           "sink", schemas.EnergySinkCreate, region_ids)

    dump_energy_components(db, dataset_id, temp_folder + "storages/", crud.energy_storage,
                           "storage", schemas.EnergyStorageCreate, region_ids)

    dump_energy_components(db, dataset_id, temp_folder + "transmissions/", crud.energy_transmission,
                           "transmission", schemas.EnergyTransmissionCreate, region_ids)

    # create zip file
    zip_file_path = os.path.join(temp_folder, "dataset.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for root, dirs, files in os.walk(temp_folder):
            acr_path = os.path.relpath(root, temp_folder)
            zip_file.write(root, acr_path)
            for file in files:
                # only copy .json and .xlsx files
                if file.endswith(".json") or file.endswith(".xlsx"):
                    zip_file.write(os.path.join(root, file), arcname=os.path.join(acr_path, file))
    return zip_file_path


def dump_energy_components(db: Session, dataset_id: int, temp_folder: str, crud_repo: CRUDBaseDependsComponent,
                           file_name: str, schema_like: Type[BaseModel], region_ids: List[int]):
    """
    Dump all energy components to folders.

    Besides the json, containing all attributes describing the specialized energy component, all time series data is
    dumped as excel files.

    :param db: database session
    :param dataset_id: dataset id
    :param temp_folder: temporary folder
    :param crud_repo: CRUD repository
    :param file_name: file name
    :param schema_like: schema like
    :param region_ids: region ids
    """

    # create sub folder if not exists
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # create key set
    fields = set(schema_like.__fields__.keys())
    fields.remove("type")

    for obj in crud_repo.get_multi_by_dataset(db, dataset_id=dataset_id):
        save_folder_name = obj.component.name.lower().replace(" ", "-")[:50]
        obj_folder = os.path.join(temp_folder, save_folder_name)
        os.makedirs(obj_folder)

        dump_dict: Dict[str, Any] = obj.component.__dict__.copy()
        dump_dict.update(obj.__dict__)

        # if obj has attribute commodity, set it with commodity.name
        if hasattr(obj, "commodity"):
            dump_dict["commodity"] = obj.commodity.name

        # if obj has attribute commodity_unit, set it with commodity.name
        if hasattr(obj, "commodity_unit"):
            dump_dict["commodity_unit"] = obj.commodity_unit.name

        # if obj has attribute conversion factors, set it with conversion factors
        if hasattr(obj, "conversion_factors"):
            factor_list = [jsonable_encoder(dict(schemas.EnergyConversionFactor.from_orm(factor)),
                                            custom_encoder={schemas.EnergyCommodity: lambda x: x.name},
                                            exclude={"id"})
                           for factor in obj.conversion_factors]
            dump_dict["conversion_factors"] = factor_list
            fields.add("conversion_factors")

        dump_json(f"{obj_folder}/{file_name}.json", fields, dump_dict)

        # dump excel files
        dump_excel_file(db, obj.ref_component, region_ids, crud.capacity_fix, f"{obj_folder}/capacityFix.xlsx")
        dump_excel_file(db, obj.ref_component, region_ids, crud.capacity_max, f"{obj_folder}/capacityMax.xlsx")
        dump_excel_file(db, obj.ref_component, region_ids, crud.operation_rate_fix,
                        f"{obj_folder}/operationRateFix.xlsx")
        dump_excel_file(db, obj.ref_component, region_ids, crud.operation_rate_max,
                        f"{obj_folder}/operationRateMax.xlsx")

        if file_name == "transmission":
            crud.energy_transmission_distance.get_dataframe(db, obj.ref_component, region_ids) \
                .to_excel(f"{obj_folder}/distances.xlsx")


def dump_json(file: str, fields: Set[str], obj: Any):
    """
    Dump the object to a json file.

    :param file: file path
    :param fields: The fields that will be included in the json.
    :param obj: The object that will be converted to a json.
    :return:
    """
    with open(file, "w", encoding='utf8') as f:
        json_obj = create_json(obj, fields)
        json.dump(json_obj, f, ensure_ascii=False, indent=4)


def create_json(obj: Any, fields: Set[str], remove_ref_fields: bool = True) -> Any:
    """
    Create a json object from the object.
    Uses jsonable_encoder to convert the object to a json string.

    :param obj: The object that will be converted to a json.
    :param fields: The fields that will be included in the json.
    :param remove_ref_fields: If true, remove the fields that start with ref_.
    :return: The json object.
    """
    if remove_ref_fields:
        fields = {field for field in fields if not field.startswith("ref_")}

    print(f"Dumping {obj} with fields {fields}")
    return jsonable_encoder(obj, include=fields, exclude_none=True)


def dump_excel_file(db: Session, component_id: int, region_ids: List[int],
                    crud_repo: CRUDBaseDependsTimeSeries, file_name: str):
    """
    Exports time series data from database to excel.

    :param db: The database session.
    :param component_id: The component id.
    :param region_ids: The region ids.
    :param crud_repo: The CRUD repository.
    :param file_name: The file name.
    """
    if len(crud_repo.get_by_component(db, component_id=component_id)) == 0:
        print(f"No data for component {component_id}. Skipping {file_name}")
        return

    crud_repo.get_dataframe(db, component_id=component_id, region_ids=region_ids).to_excel(file_name)
