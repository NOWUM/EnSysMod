import json
from tempfile import TemporaryFile
from typing import List
from zipfile import ZipFile

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import RegionCreate, RegionUpdate


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

    # process region.json
    region_file = zip_archive.open("regions.json")
    process_regions_file(region_file, dataset_id, db)

    # print all files in the zip archive
    for file in zip_archive.namelist():
        print(file)


def process_regions_file(regions_file: TemporaryFile, dataset_id: int, db: Session):
    """
    Processes a region file and adds the regions to the dataset in database.

    :param regions_file: File to process
    :param dataset_id: ID of the dataset to add the regions to
    :param db: Database session
    """
    # map region_file.json to List[RegionCreate]
    regions: List[RegionCreate] = json.load(regions_file)
    print(regions)
    for region in regions:
        existing_region = crud.region.get_by_dataset_and_name(db, dataset_id=dataset_id, name=region.name)
        if existing_region is not None:
            print(f"Region {region.name} doesn't exists in dataset {dataset_id}. Creating...")
            region.ref_dataset = dataset_id
            crud.region.create(db, region=region)
        else:
            print(f"Region {region.name} already exists in database. Updating...")
            update = RegionUpdate(**region.dict())
            update.ref_dataset = dataset_id
            crud.region.update(db, region_id=existing_region.id, region=update)
