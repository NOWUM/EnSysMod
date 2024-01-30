import json
import re
from pathlib import Path
from shutil import make_archive
from tempfile import TemporaryDirectory
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import EXCEL_FILE_TYPES, FOLDER_TYPES, JSON_FILE_TYPES
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.schemas import EnergyCommoditySchema, EnergyConversionFactorSchema
from ensysmod.schemas.base_schema import CreateSchema
from ensysmod.utils.utils import create_temp_file


def export_data(db: Session, dataset_id: int) -> Path:
    """
    Create a zip file for the dataset.

    :param db: database session
    :param dataset_id: dataset id
    :param export_dir: export directory for the dataset
    :return: Path to zip file
    """
    with TemporaryDirectory(prefix="ensysmod_") as export_dir:
        export_dir = Path(export_dir)
        # export regions.json and commodities.json
        for json_file in JSON_FILE_TYPES:
            dump_json(
                obj=json_file.crud_repo.get_multi_by_dataset(db, dataset_id=dataset_id),
                fields=set(json_file.create_schema.model_fields),
                file_path=Path(export_dir, json_file.file_name),
            )

        # export component folders
        for folder in FOLDER_TYPES:
            dump_energy_component(
                db=db,
                dataset_id=dataset_id,
                component_type_folder=Path(export_dir, folder.folder_name),
                file_name=folder.file_name,
                crud_repo=folder.crud_repo,
                create_schema=folder.create_schema,
            )

        temp_file_path = create_temp_file(prefix="ensysmod_dataset_", suffix=".zip")
        base_name = str(temp_file_path.with_suffix(""))
        return Path(make_archive(base_name=base_name, format="zip", root_dir=export_dir))


def dump_energy_component(
    *,
    db: Session,
    dataset_id: int,
    component_type_folder: Path,
    file_name: str,
    crud_repo: CRUDBaseDependsComponent,
    create_schema: type[CreateSchema],
) -> None:
    """
    Dump all energy components to folders.

    :param db: database session
    :param dataset_id: dataset id
    :param component_type_folder: component type folder
    :param file_name: name of the component .json file
    :param crud_repo: CRUD repository
    :param create_schema: create schema
    """
    fields = set(create_schema.model_fields)
    fields.remove("type")

    for component in crud_repo.get_multi_by_dataset(db, dataset_id=dataset_id):
        component_name = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "_", component.component.name)
        component_folder = Path(component_type_folder, component_name)
        component_folder.mkdir(parents=True)

        component_dict: dict[str, Any] = component.component.__dict__.copy()
        component_dict.update(component.__dict__)

        # replace commodity object model with the commodity name
        if hasattr(component, "commodity"):
            component_dict["commodity"] = component.commodity.name

        # replace conversion factors object model with the conversion factors in json list format
        if hasattr(component, "conversion_factors"):
            component_dict["conversion_factors"] = conversion_factors_json(component)

        # dump component json file
        dump_json(obj=component_dict, fields=fields, file_path=Path(component_folder, file_name))

        # dump excel files
        for excel_file in EXCEL_FILE_TYPES:
            dump_excel_file(
                db=db,
                component_id=component.ref_component,
                crud_repo=excel_file.crud_repo,
                file_path=Path(component_folder, excel_file.file_name),
            )


def conversion_factors_json(component) -> list[dict[str, Any]]:
    return [
        jsonable_encoder(
            obj=dict(EnergyConversionFactorSchema.model_validate(factor)),
            include={"conversion_factor", "commodity"},
            custom_encoder={EnergyCommoditySchema: lambda x: x.name},
        )
        for factor in component.conversion_factors
    ]


def dump_json(*, obj: Any, fields: set[str], file_path: Path) -> None:
    """
    Dump the object to a json file.

    :param file_path: file path
    :param fields: The fields that will be included in the json.
    :param obj: The object that will be converted to a json.
    """
    fields = {field for field in fields if not field.startswith("ref_")}
    json_obj = jsonable_encoder(obj, include=fields)

    with file_path.open(mode="w", encoding="utf_8") as file:
        json.dump(json_obj, file, ensure_ascii=False, indent=4)


def dump_excel_file(*, db: Session, component_id: int, crud_repo: CRUDBaseDependsExcel, file_path: Path) -> None:
    """
    Export excel data from database to an excel file.

    :param db: The database session.
    :param component_id: The component id.
    :param crud_repo: The CRUD repository.
    :param file_path: The file path.
    """
    if len(crud_repo.get_multi_by_component(db, component_id=component_id)) != 0:
        crud_repo.get_dataframe(db, component_id=component_id).to_excel(file_path)
