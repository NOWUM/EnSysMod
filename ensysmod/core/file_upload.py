import json
from tempfile import TemporaryFile
from typing import List, Dict, Any, Type
from zipfile import ZipFile

import pandas as pd
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from ensysmod import crud, schemas
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries


def create_or_update_named_entity(crud_repo: CRUDBaseDependsDataset, db: Session, request: Any):
    """
    This function creates or updates an object inside the given crud repository.

    :param crud_repo: The crud repository.
    :param db: The database session.
    :param request: The request.
    :return: The created or updated object.
    """
    existing_object = crud_repo.get_by_dataset_and_name(db, dataset_id=request.ref_dataset, name=request.name)
    if existing_object is None:
        print(f"{request.name} doesn't exists in dataset {request.ref_dataset}. Creating...")
        return crud_repo.create(db, obj_in=request)
    else:
        print(f"{request.name} already exists in database. Updating...")
        return crud_repo.update(db, obj_in=request, db_obj=existing_object)


def create_or_update_time_series(crud_repo: CRUDBaseDependsTimeSeries, db: Session, request: Any):
    """
    This function creates or updates an object inside the given crud repository.

    :param crud_repo: The crud repository.
    :param db: The database session.
    :param request: The request.
    :return: The created or updated object.
    """
    # TODO : Check if the time series already exists
    return crud_repo.create(db, obj_in=request)


def map_with_dataset_id(create_model: Type[BaseModel], json_dict: Dict, dataset_id: int):
    """
    Maps a json dict to a dict with the ref_dataset key set to the given dataset_id.
    """
    json_dict["ref_dataset"] = dataset_id
    print(json_dict)
    return create_model.parse_obj(json_dict)


def process_dataset_zip_archive(zip_archive: ZipFile, dataset_id: int, db: Session):
    """
    Processes a zip archive and adds the components to the dataset in database.

    The zip archive must contain the following files:
    - commodities.json representing a List[CommodityCreate]
    - regions.json representing a List[RegionCreate]

    The zip archive can contain the following folders:
    - conversions
    - sinks
    - sources
    - storages
    - transmissions

    :param zip_archive: Zip archive to process
    :param dataset_id: ID of the dataset to add the components to
    :param db: Database session
    """

    if "commodities.json" not in zip_archive.namelist():
        raise ValueError("Zip archive must contain commodities.json")

    if "regions.json" not in zip_archive.namelist():
        raise ValueError("Zip archive must contain regions.json")

    # process region.json and commodities.json
    process_list_file(zip_archive.open("regions.json"), db, dataset_id, crud.region, schemas.RegionCreate)
    process_list_file(zip_archive.open("commodities.json"), db, dataset_id, crud.energy_commodity,
                      schemas.EnergyCommodityCreate)

    # process conversions
    process_components_folder(zip_archive, folder_name="conversions/", component_file_name="conversion.json",
                              dataset_id=dataset_id, db=db, crud_repo=crud.energy_conversion,
                              create_model=schemas.EnergyConversionCreate)
    process_components_folder(zip_archive, folder_name="sinks/", component_file_name="sink.json",
                              dataset_id=dataset_id, db=db, crud_repo=crud.energy_sink,
                              create_model=schemas.EnergySinkCreate)
    process_components_folder(zip_archive, folder_name="sources/", component_file_name="source.json",
                              dataset_id=dataset_id, db=db, crud_repo=crud.energy_source,
                              create_model=schemas.EnergySourceCreate)
    process_components_folder(zip_archive, folder_name="storages/", component_file_name="storage.json",
                              dataset_id=dataset_id, db=db, crud_repo=crud.energy_storage,
                              create_model=schemas.EnergyStorageCreate)
    process_components_folder(zip_archive, folder_name="transmissions/", component_file_name="transmission.json",
                              dataset_id=dataset_id, db=db, crud_repo=crud.energy_transmission,
                              create_model=schemas.EnergyTransmissionCreate)


def process_list_file(file: TemporaryFile, db: Session, dataset_id: int, crud_repo: CRUDBaseDependsComponent,
                      create_model: Type[BaseModel]):
    """
    Processes a file containing a list of objects.
    Each object gets a ref_dataset key set to the given dataset_id and gets created or updated in the database.

    :param file: File to process
    :param db: Database session
    :param dataset_id: ID of the dataset to add the components to
    :param crud_repo: CRUD repository to use
    :param create_model: Create model to use
    """
    dicts: List[dict] = json.load(file)
    for single_dict in dicts:
        create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_model, single_dict, dataset_id))


def process_components_folder(zip_archive: ZipFile,
                              folder_name: str, component_file_name: str,
                              dataset_id: int,
                              db: Session,
                              crud_repo: CRUDBaseDependsComponent, create_model: Type[BaseModel]):
    """
    Processes a folder and adds the components to the dataset in database.
    """
    if folder_name not in zip_archive.namelist():
        # raise ValueError(f"Folder {folder_name}
        print(f"Folder {folder_name} doesn't exists in zip archive. Skipping...")
        return

    # get all sub folder names inside folder_name
    sub_folder_names = [name for name in zip_archive.namelist() if name.startswith(folder_name)
                        and name.count("/") == 2
                        and name.endswith("/")]

    for sub_folder_name in sub_folder_names:
        json_dict = json.load(zip_archive.open(sub_folder_name + component_file_name))
        create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_model, json_dict, dataset_id))

        # check if operationRateFix.xlsx exists in sub_folder_name
        if sub_folder_name + "operationRateFix.xlsx" in zip_archive.namelist():
            # process operationRateFix.xlsx
            process_excel_file(zip_archive.open(sub_folder_name + "operationRateFix.xlsx"), db, dataset_id,
                               json_dict["name"], "fix_operation_rates", crud_repo=crud.operation_rate_fix,
                               create_model=schemas.OperationRateFixCreate)


def process_excel_file(file: TemporaryFile, db: Session, dataset_id: int, component_name: str, data_key: str,
                       crud_repo: CRUDBaseDependsTimeSeries, create_model: Type[BaseModel]):
    """
    Processes an excel file and adds the time series to the database.

    :param file: File to process
    :param db: Database session
    :param dataset_id: ID of the dataset to add the components to
    :param component_name: Name of the component to add the time series to
    :param data_key: Key of the data to add the time series to
    :param crud_repo: CRUD repository to use
    :param create_model: Create model to use
    """
    df = pd.read_excel(file)

    # for each column, create a time series
    for column in df.columns:
        request_dict = {data_key: df[column].tolist(), "region": column, "component": component_name}
        create_request = map_with_dataset_id(create_model, request_dict, dataset_id)
        create_or_update_time_series(crud_repo, db, create_request)
