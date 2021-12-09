import json
from tempfile import TemporaryFile
from typing import List
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import RegionCreate


def process_dataset_zip_archive(zip_archive: ZipFile, dataset_id: int, db: Session):
    """
    Processes a zip archive and adds the components to the dataset in database.

    The zip archive must contain the following files:
    - commodities.json representing a List[CommodityCreate]
    - region.json representing a List[RegionCreate]

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

    # print all files in the zip archive
    for file in zip_archive.namelist():
        print(file)


def process_region_file(region_file: TemporaryFile, dataset_id: int, db: Session):
    """
    Processes a region file and adds the regions to the dataset in database.

    :param region_file: File to process
    :param dataset_id: ID of the dataset to add the regions to
    :param db: Database session
    """
    # map region_file.json to List[RegionCreate]
    regions: List[RegionCreate] = json.load(region_file)
    for region in regions:
        existing_region = crud.region.get_by_dataset_and_name(db, dataset_id=dataset_id, name=region.name)
        if existing_region is not None:
            region.ref_dataset = dataset_id
            crud.region.create(db, region=region)
