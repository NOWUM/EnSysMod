from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate
from tests.utils.data_generator import random_existing_dataset, fixed_existing_dataset
from tests.utils.utils import random_lower_string


def random_region_create(db: Session) -> RegionCreate:
    dataset = random_existing_dataset(db)
    return RegionCreate(name=f"Region-{dataset.id}-{random_lower_string()}",
                        ref_dataset=dataset.id)


def random_existing_region(db: Session) -> Region:
    create_request = random_region_create(db)
    return crud.region.create(db=db, obj_in=create_request)


def fixed_region_create(db: Session) -> RegionCreate:
    dataset = fixed_existing_dataset(db)
    return RegionCreate(name=f"Region-{dataset.id}-Fixed",
                        ref_dataset=dataset.id)


def fixed_alternative_region_create(db: Session) -> RegionCreate:
    dataset = fixed_existing_dataset(db)
    return RegionCreate(name=f"Region-{dataset.id}-Fixed-alternative",
                        ref_dataset=dataset.id)


def fixed_alternative_alternative_region_create(db: Session) -> RegionCreate:
    dataset = fixed_existing_dataset(db)
    return RegionCreate(name=f"Region-{dataset.id}-Fixed-alternative-alternative",
                        ref_dataset=dataset.id)


def fixed_existing_region(db: Session) -> Region:
    create_request = fixed_region_create(db)
    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset, name=create_request.name)
    if region is None:
        region = crud.region.create(db=db, obj_in=create_request)
    return region


def fixed_alternative_existing_region(db: Session) -> Region:
    create_request = fixed_alternative_region_create(db)
    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset, name=create_request.name)
    if region is None:
        region = crud.region.create(db=db, obj_in=create_request)
    return region


def fixed_alternative_alternative_existing_region(db: Session) -> Region:
    create_request = fixed_alternative_alternative_region_create(db)
    region = crud.region.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset, name=create_request.name)
    if region is None:
        region = crud.region.create(db=db, obj_in=create_request)
    return region
