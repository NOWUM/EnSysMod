import json
from typing import Any, List, Set, Dict, Union
from zipfile import ZipFile

from fastapi.encoders import jsonable_encoder
from pydantic.fields import ModelField
from sqlalchemy.orm import Session

from ensysmod import crud, schemas


def export_data(db: Session, dataset_id: int, temp_folder: str) -> str:
    """
    Create a zip file for the dataset.

    :param db: database session
    :param dataset_id: dataset id
    :param temp_folder: temporary folder
    :return: Path to zip file
    """

    # create commodities.json
    dump_json(f"{temp_folder}/commodities.json", schemas.EnergyCommodityCreate.__fields__,
              crud.energy_commodity.get_multi_by_dataset(db, dataset_id=dataset_id))

    # create regions.json
    dump_json(f"{temp_folder}/regions.json", schemas.RegionCreate.__fields__,
              crud.region.get_multi_by_dataset(db, dataset_id=dataset_id))

    # create zip file
    zip_file_path = f"{temp_folder}\\data.zip"
    # zip all contents of temp folder with folder structure
    with ZipFile(zip_file_path, "w") as zip_file:
        zip_file.write(f"{temp_folder}/commodities.json", "commodities.json")
        zip_file.write(f"{temp_folder}/regions.json", "regions.json")
    return zip_file_path


def dump_json(file: str, cls, obj: Any):
    """
    Dump the object to a json file.

    :param file:
    :param cls:
    :param obj:
    :return:
    """
    with open(file, "w") as f:
        json.dump(jsonable_encoder(obj), f, ensure_ascii=False, indent=4)
