import json
from tempfile import TemporaryFile
from typing import List, Dict, Any, Type
from zipfile import ZipFile

import pandas as pd
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ensysmod import crud, schemas
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.schemas import ZipArchiveUploadResult, FileStatus, FileUploadResult


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
    return create_model.parse_obj(json_dict)


def process_dataset_zip_archive(zip_archive: ZipFile, dataset_id: int, db: Session) -> ZipArchiveUploadResult:
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

    file_results: List[FileUploadResult] = []

    # process region.json and commodities.json
    region_result = process_list_file(zip_archive.open("regions.json"), db, dataset_id, crud.region,
                                      schemas.RegionCreate)
    file_results.append(region_result)
    commodity_result = process_list_file(zip_archive.open("commodities.json"), db, dataset_id, crud.energy_commodity,
                                         schemas.EnergyCommodityCreate)
    file_results.append(commodity_result)

    # process conversions
    conversion_results = process_components_folder(zip_archive, folder_name="conversions/",
                                                   component_file_name="conversion.json",
                                                   dataset_id=dataset_id, db=db, crud_repo=crud.energy_conversion,
                                                   create_model=schemas.EnergyConversionCreate)
    file_results.extend(conversion_results)
    sink_results = process_components_folder(zip_archive, folder_name="sinks/", component_file_name="sink.json",
                                             dataset_id=dataset_id, db=db, crud_repo=crud.energy_sink,
                                             create_model=schemas.EnergySinkCreate)
    file_results.extend(sink_results)
    source_results = process_components_folder(zip_archive, folder_name="sources/", component_file_name="source.json",
                                               dataset_id=dataset_id, db=db, crud_repo=crud.energy_source,
                                               create_model=schemas.EnergySourceCreate)
    file_results.extend(source_results)
    storage_results = process_components_folder(zip_archive, folder_name="storages/",
                                                component_file_name="storage.json",
                                                dataset_id=dataset_id, db=db, crud_repo=crud.energy_storage,
                                                create_model=schemas.EnergyStorageCreate)
    file_results.extend(storage_results)
    transmission_results = process_components_folder(zip_archive, folder_name="transmissions/",
                                                     component_file_name="transmission.json",
                                                     dataset_id=dataset_id, db=db, crud_repo=crud.energy_transmission,
                                                     create_model=schemas.EnergyTransmissionCreate,
                                                     matrix_files=True)
    file_results.extend(transmission_results)

    if all(file_result.status == FileStatus.OK for file_result in file_results):
        return ZipArchiveUploadResult(status=FileStatus.OK, file_results=file_results)
    else:
        return ZipArchiveUploadResult(status=FileStatus.ERROR, file_results=file_results)


def process_list_file(file: TemporaryFile, db: Session, dataset_id: int, crud_repo: CRUDBaseDependsComponent,
                      create_model: Type[BaseModel]) -> FileUploadResult:
    """
    Processes a file containing a list of objects.
    Each object gets a ref_dataset key set to the given dataset_id and gets created or updated in the database.

    :param file: File to process
    :param db: Database session
    :param dataset_id: ID of the dataset to add the components to
    :param crud_repo: CRUD repository to use
    :param create_model: Create model to use
    """
    try:
        dicts: List[dict] = json.load(file)
        for single_dict in dicts:
            create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_model, single_dict, dataset_id))
        return FileUploadResult(status=FileStatus.OK, file=file.name, message=f"Processed {len(dicts)} objects.")
    except Exception as e:
        return FileUploadResult(status=FileStatus.ERROR, file=file.name, message=str(e))


def process_components_folder(zip_archive: ZipFile,
                              folder_name: str, component_file_name: str,
                              dataset_id: int,
                              db: Session,
                              crud_repo: CRUDBaseDependsComponent,
                              create_model: Type[BaseModel], matrix_files: bool = False) -> List[FileUploadResult]:
    """
    Processes a folder and adds the components to the dataset in database.
    """
    if folder_name not in zip_archive.namelist():
        return [FileUploadResult(status=FileStatus.SKIPPED, file=folder_name,
                                 message=f"Folder {folder_name} doesn't exists in zip archive. Skipping...")]

    file_results: List[FileUploadResult] = []

    # get all sub folder names inside folder_name
    sub_folder_names = [name for name in zip_archive.namelist() if name.startswith(folder_name)
                        and name.count("/") == 2
                        and name.endswith("/")]

    for sub_folder_name in sub_folder_names:
        component_file = sub_folder_name + component_file_name
        try:
            json_dict = json.load(zip_archive.open(component_file))
            create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_model, json_dict, dataset_id))
            file_results.append(FileUploadResult(status=FileStatus.OK, file=component_file,
                                                 message=f"Processed {component_file}"))
        except Exception as e:
            file_results.append(FileUploadResult(status=FileStatus.ERROR, file=component_file, message=str(e)))
            file_results.append(FileUploadResult(status=FileStatus.SKIPPED, file=sub_folder_name,
                                                 message=f"Skipped files in folder {sub_folder_name} due to error."))
            continue

        if matrix_files:
            results = process_sub_folder_matrix_files(zip_archive, sub_folder_name, db, dataset_id, json_dict["name"])
        else:
            results = process_sub_folder_files(zip_archive, sub_folder_name, db, dataset_id, json_dict["name"])
        file_results.extend(results)

    return file_results


def process_sub_folder_files(zip_archive: ZipFile, sub_folder_name: str, db: Session, dataset_id: int,
                             component_name: str):
    file_results: List[FileUploadResult] = []

    # check if operationRateFix.xlsx exists in sub_folder_name
    if sub_folder_name + "operationRateFix.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_excel_file(zip_archive.open(sub_folder_name + "operationRateFix.xlsx"),
                                               db, dataset_id,
                                               component_name, "fix_operation_rates",
                                               crud_repo=crud.operation_rate_fix,
                                               create_model=schemas.OperationRateFixCreate))

    # check if operationRateMax.xlsx exists in sub_folder_name
    if sub_folder_name + "operationRateMax.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_excel_file(zip_archive.open(sub_folder_name + "operationRateMax.xlsx"),
                                               db, dataset_id,
                                               component_name, "max_operation_rates",
                                               crud_repo=crud.operation_rate_max,
                                               create_model=schemas.OperationRateMaxCreate))

    # check if capacityFix.xlsx exists in sub_folder_name
    if sub_folder_name + "capacityFix.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_excel_file(zip_archive.open(sub_folder_name + "capacityFix.xlsx"),
                                               db, dataset_id,
                                               component_name, "fix_capacities",
                                               crud_repo=crud.capacity_fix,
                                               create_model=schemas.CapacityFixCreate))

    # check if capacityMax.xlsx exists in sub_folder_name
    if sub_folder_name + "capacityMax.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_excel_file(zip_archive.open(sub_folder_name + "capacityMax.xlsx"),
                                               db, dataset_id,
                                               component_name, "max_capacities",
                                               crud_repo=crud.capacity_max,
                                               create_model=schemas.CapacityMaxCreate))
    return file_results


def process_sub_folder_matrix_files(zip_archive: ZipFile, sub_folder_name: str, db: Session, dataset_id: int,
                                    component_name: str):
    file_results: List[FileUploadResult] = []

    # check if capacityFix.xlsx exists in sub_folder_name
    if sub_folder_name + "capacityFix.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_matrix_excel_file(zip_archive.open(sub_folder_name + "capacityFix.xlsx"),
                                                      db, dataset_id,
                                                      component_name, "fix_capacities",
                                                      crud_repo=crud.capacity_fix,
                                                      create_model=schemas.CapacityFixCreate))

    # check if capacityMax.xlsx exists in sub_folder_name
    if sub_folder_name + "capacityMax.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_matrix_excel_file(zip_archive.open(sub_folder_name + "capacityMax.xlsx"),
                                                      db, dataset_id,
                                                      component_name, "max_capacities",
                                                      crud_repo=crud.capacity_max,
                                                      create_model=schemas.CapacityMaxCreate))

    # check if distances.xlsx exists in sub_folder_name
    if sub_folder_name + "distances.xlsx" in zip_archive.namelist():
        # process operationRateFix.xlsx
        file_results.append(process_matrix_excel_file(zip_archive.open(sub_folder_name + "distances.xlsx"),
                                                      db, dataset_id,
                                                      component_name, "distance",
                                                      crud_repo=crud.energy_transmission_distance,
                                                      create_model=schemas.EnergyTransmissionDistanceCreate,
                                                      as_list=False, region_key="region_from"))
    return file_results


def process_excel_file(file: TemporaryFile, db: Session, dataset_id: int, component_name: str, data_key: str,
                       crud_repo: CRUDBaseDependsTimeSeries, create_model: Type[BaseModel]) -> FileUploadResult:
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
    try:
        df: pd.DataFrame = pd.read_excel(file)

        # for each column, create a time series
        for column in df.columns:
            if column == "Unnamed: 0":
                # Skip first unnamed column, because this is might be the index
                continue
            request_dict = {data_key: df[column].tolist(), "region": column, "component": component_name}
            create_request = map_with_dataset_id(create_model, request_dict, dataset_id)
            create_or_update_time_series(crud_repo, db, create_request)
        return FileUploadResult(status=FileStatus.OK, file=file.name, message=f"Processed {file.name}")
    except Exception as e:
        return FileUploadResult(status=FileStatus.ERROR, file=file.name, message=str(e))


def process_matrix_excel_file(file: TemporaryFile, db: Session, dataset_id: int, component_name: str, data_key: str,
                              crud_repo: CRUDBaseDependsTimeSeries, create_model: Type[BaseModel],
                              as_list: bool = True, region_key: str = "region") -> FileUploadResult:
    """
    Processes an excel file and adds the matrix data (region_from / region_to) to the database.

    :param file: File to process
    :param db: Database session
    :param dataset_id: ID of the dataset to add the components to
    :param component_name: Name of the component to add the time series to
    :param data_key: Key of the data to add the time series to
    :param crud_repo: CRUD repository to use
    :param create_model: Create model to use
    :param as_list: If true, the data is returned as a list, otherwise as a single float
    :param region_key: Key of the region to use
    """
    try:
        df: pd.DataFrame = pd.read_excel(file)

        # determine the labels (region_from and region_to) of rows and columns
        regions = df.iloc[:, 0].tolist()
        df.drop(df.columns[0], axis=1, inplace=True)
        regions_to = df.columns.tolist()

        # for each element of matrix
        for i in range(0, len(df.values)):
            for j in range(0, len(df.values[i])):
                request_dict = {region_key: regions[i], "region_to": regions_to[j], "component": component_name}
                if as_list:
                    request_dict[data_key] = [df.values[i][j]]
                else:
                    request_dict[data_key] = df.values[i][j]
                create_request = map_with_dataset_id(create_model, request_dict, dataset_id)
                create_or_update_time_series(crud_repo, db, create_request)
        return FileUploadResult(status=FileStatus.OK, file=file.name, message=f"Processed {file.name}")
    except Exception as e:
        return FileUploadResult(status=FileStatus.ERROR, file=file.name, message=str(e))
