import json
from typing import Any
from zipfile import ZipFile

import pandas as pd
from crud.base import CreateSchemaType
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile

from ensysmod.core.file_folder_types import EXCEL_FILE_TYPES, FOLDER_TYPES, JSON_FILE_TYPES
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix
from ensysmod.schemas import FileStatus, FileUploadResult, ZipArchiveUploadResult


def create_or_update_named_entity(crud_repo: CRUDBaseDependsDataset, db: Session, request: CreateSchemaType):
    """
    This function creates or updates an object inside the given crud repository.

    :param crud_repo: The crud repository.
    :param db: The database session.
    :param request: The request.
    :return: The created or updated object.
    """
    existing_object = crud_repo.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing_object is not None:
        print(f"{request.name} already exists in database. Updating...")
        return crud_repo.update(db, obj_in=request, db_obj=existing_object)

    print(f"{request.name} doesn't exists in dataset {request.ref_dataset}. Creating...")
    return crud_repo.create(db, obj_in=request)


def map_with_dataset_id(create_schema: type[CreateSchemaType], json_dict: dict, dataset_id: int) -> CreateSchemaType:
    """
    Maps a json dict to a dict with the ref_dataset key set to the given dataset_id.
    """
    json_dict["ref_dataset"] = dataset_id
    return create_schema.parse_obj(json_dict)


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

    file_results: list[FileUploadResult] = []

    # process regions.json and commodities.json
    for json_file in JSON_FILE_TYPES:
        if json_file.file_name not in zip_archive.namelist():
            raise ValueError(f"Zip archive must contain {json_file.file_name}!")
        file_results.append(
            process_json_list_file(
                db=db,
                dataset_id=dataset_id,
                zip_archive=zip_archive,
                file_name=json_file.file_name,
                crud_repo=json_file.crud_repo,
                create_schema=json_file.create_schema,
            ),
        )

    # process component folders
    for folder in FOLDER_TYPES:
        folder_name: str = folder.folder_name + "/"  # folder name in the zip has / at the end
        file_results.extend(
            process_components_folder(
                db=db,
                dataset_id=dataset_id,
                zip_archive=zip_archive,
                folder_name=folder_name,
                component_file_name=folder.file_name,
                crud_repo=folder.crud_repo,
                create_schema=folder.create_schema,
                as_matrix=folder.as_matrix,
            ),
        )

    if all(file_result.status == FileStatus.OK for file_result in file_results):
        return ZipArchiveUploadResult(status=FileStatus.OK, file_results=file_results)

    return ZipArchiveUploadResult(status=FileStatus.ERROR, file_results=file_results)


def process_json_list_file(
    *,
    db: Session,
    dataset_id: int,
    zip_archive: ZipFile,
    file_name: str,
    crud_repo: CRUDBaseDependsDataset,
    create_schema: type[CreateSchemaType],
) -> FileUploadResult:
    """
    Process a json file containing a list of objects.
    Each object gets a ref_dataset key set to the given dataset_id and gets created or updated in the database.

    :param db: Database session
    :param dataset_id: ID of the dataset to add the components to
    :param zip_archive: Zip archive to process
    :param file_name: File name to process
    :param crud_repo: CRUD repository to use
    :param create_schema: Create schema to use
    """
    try:
        with zip_archive.open(file_name) as content:
            dicts: list[dict] = json.load(content)
        for single_dict in dicts:
            create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_schema, single_dict, dataset_id))
        return FileUploadResult(status=FileStatus.OK, file=file_name, message=f"Processed {len(dicts)} objects.")
    except Exception as e:
        return FileUploadResult(status=FileStatus.ERROR, file=file_name, message=str(e))


def process_components_folder(
    *,
    db: Session,
    dataset_id: int,
    zip_archive: ZipFile,
    folder_name: str,
    component_file_name: str,
    crud_repo: CRUDBaseDependsComponent,
    create_schema: type[CreateSchemaType],
    as_matrix: bool = False,
) -> list[FileUploadResult]:
    """
    Process a folder and add the components to the dataset in database.
    """
    if folder_name not in zip_archive.namelist():
        return [
            FileUploadResult(status=FileStatus.SKIPPED, file=folder_name, message=f"Folder {folder_name} doesn't exists in zip archive. Skipping..."),
        ]

    file_results: list[FileUploadResult] = []

    sub_folder_names: list[str] = [
        name for name in zip_archive.namelist() if name.startswith(folder_name) and name.count("/") == 2 and name.endswith("/")
    ]

    for sub_folder_name in sub_folder_names:
        component_file_path: str = sub_folder_name + component_file_name
        try:
            with zip_archive.open(component_file_path) as content:
                json_dict = json.load(content)
            create_or_update_named_entity(crud_repo, db, map_with_dataset_id(create_schema, json_dict, dataset_id))
            file_results.append(FileUploadResult(status=FileStatus.OK, file=component_file_path, message=f"Processed {component_file_path}"))
        except Exception as e:
            file_results.append(FileUploadResult(status=FileStatus.ERROR, file=component_file_path, message=str(e)))
            file_results.append(
                FileUploadResult(status=FileStatus.SKIPPED, file=sub_folder_name, message=f"Skipped files in folder {sub_folder_name} due to error."),
            )
            continue

        file_results.extend(
            process_sub_folder_files(
                zip_archive=zip_archive,
                db=db,
                dataset_id=dataset_id,
                component_name=json_dict["name"],
                sub_folder_name=sub_folder_name,
                as_matrix=as_matrix,
            ),
        )

    return file_results


def process_sub_folder_files(
    *,
    db: Session,
    dataset_id: int,
    zip_archive: ZipFile,
    component_name: str,
    sub_folder_name: str,
    as_matrix: bool = False,
) -> list[FileUploadResult]:
    file_results: list[FileUploadResult] = []

    sub_folder_file_paths = [path for path in zip_archive.namelist() if path.startswith(sub_folder_name) and path.endswith(".xlsx")]
    if len(sub_folder_file_paths) == 0:
        return file_results

    for excel_file in EXCEL_FILE_TYPES:
        file_path: str = sub_folder_name + excel_file.file_name
        if file_path in sub_folder_file_paths:
            file_results.append(
                process_excel_file(
                    file=(zip_archive, file_path),
                    db=db,
                    dataset_id=dataset_id,
                    component_name=component_name,
                    crud_repo=excel_file.crud_repo,
                    create_schema=excel_file.create_schema,
                    as_list=excel_file.as_list,
                    as_matrix=as_matrix,
                ),
            )
    return file_results


def process_excel_file(
    *,
    file: UploadFile | tuple[ZipFile, str],
    db: Session,
    dataset_id: int,
    component_name: str,
    crud_repo: CRUDBaseDependsMatrix,
    create_schema: type[BaseModel],
    as_list: bool = False,
    as_matrix: bool = False,
) -> FileUploadResult:
    """
    Process an excel file and add it to the database.
    If as_list is true, the data is returned as a list of floats, otherwise as a single float.
    If as_matrix is true, the file is read as a matrix, otherwise it is read per column.
    """
    try:
        if isinstance(file, UploadFile):
            file_path = file.filename if file.filename is not None else ""
            content = file.file.read()
            df: pd.DataFrame = pd.read_excel(content, engine="openpyxl")
        elif isinstance(file, tuple):
            zip_archive, file_path= file
            with zip_archive.open(file_path) as content:
                df: pd.DataFrame = pd.read_excel(content, engine="openpyxl")

        if as_matrix:
            # determine the labels (region and region_to) of rows and columns
            regions = df.iloc[:, 0].tolist()
            df.drop(df.columns[0], axis=1, inplace=True)
            regions_to = df.columns.tolist()

            df_array = df.to_numpy()
            # for each element of matrix
            for i in range(len(df_array)):
                for j in range(len(df_array[i])):
                    data: list[float] | float = [df_array[i][j]] if as_list else df_array[i][j]

                    request_dict = {
                        crud_repo.data_column: data,
                        "component": component_name,
                        "region": regions[i],
                        "region_to": regions_to[j],
                    }

                    create_request = map_with_dataset_id(create_schema, request_dict, dataset_id)
                    crud_repo.create(db=db, obj_in=create_request)
        else:
            for column in df.columns:
                if column == "Unnamed: 0":
                    continue  # Skip first unnamed column, because this is might be the index
                if not as_list and len(df) != 1:
                    raise ValueError(f"Only one row is expected, but {len(df)} were given.")

                data: list[float] | float = df[column].tolist() if as_list else df[column][0]

                request_dict: dict[str, Any] = {
                    crud_repo.data_column: data,
                    "component": component_name,
                    "region": column,
                }

                create_request = map_with_dataset_id(create_schema, request_dict, dataset_id)
                crud_repo.create(db=db, obj_in=create_request)

        return FileUploadResult(status=FileStatus.OK, file=file_path, message=f"Processed {file_path}")

    except Exception as e:
        return FileUploadResult(status=FileStatus.ERROR, file=file_path, message=str(e))
