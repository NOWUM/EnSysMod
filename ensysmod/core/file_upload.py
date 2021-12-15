import json
from tempfile import TemporaryFile
from typing import List
from zipfile import ZipFile

from pydantic.json import Dict
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import RegionCreate, RegionUpdate, EnergyCommodityCreate, EnergyCommodityUpdate


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
    commodity_file = zip_archive.open("commodities.json")
    process_commodities_file(commodity_file, dataset_id, db)

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

    def map_region(json_dict: Dict) -> RegionCreate:
        """
            Maps a json dict to a RegionCreate object.
            """
        json_dict["ref_dataset"] = dataset_id
        return RegionCreate.parse_obj(json_dict)

    regions: List[RegionCreate] = json.load(regions_file,
                                            object_hook=lambda d: map_region(d))
    for region in regions:
        existing_region = crud.region.get_by_dataset_and_name(db, dataset_id=dataset_id, name=region.name)
        if existing_region is None:
            print(f"Region {region.name} doesn't exists in dataset {dataset_id}. Creating...")
            crud.region.create(db, obj_in=region)
        else:
            print(f"Region {region.name} already exists in database. Updating...")
            update = RegionUpdate(**region.dict())
            crud.region.update(db, obj_in=update, db_obj=existing_region)


def process_commodities_file(commodities_file: TemporaryFile, dataset_id: int, db: Session):
    """
            Processes a commodities file and adds the commodities to the dataset in database.

            :param commodities_file: File to process
            :param dataset_id: ID of the dataset to add the regions to
            :param db: Database session
            """

    def map_commodities(json_dict: Dict) -> EnergyCommodityCreate:
        """
            Maps a json dict to a EnergyCommodityCreate object.
            """
        json_dict["ref_dataset"] = dataset_id
        return EnergyCommodityCreate.parse_obj(json_dict)

    commodities: List[EnergyCommodityCreate] = json.load(commodities_file,
                                                         object_hook=lambda d: map_commodities(d))
    for commodity in commodities:
        existing_commodities = crud.energy_commodity.get_by_dataset_and_name(db, dataset_id=dataset_id,
                                                                             name=commodity.name)
        if existing_commodities is None:
            print(f"Commodity {commodity.name} doesn't exists in dataset {dataset_id}. Creating...")
            crud.energy_commodity.create(db, obj_in=commodity)
        else:
            print(f"Commodity {commodity.name} already exists in database. Updating...")
            update = EnergyCommodityUpdate(**commodity.dict())
            crud.energy_commodity.update(db, obj_in=update, db_obj=existing_commodities)
