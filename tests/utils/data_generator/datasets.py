from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate
from tests.utils.utils import random_lower_string, create_random_user


def random_dataset_create() -> DatasetCreate:
    """
    Generates a random dataset create request.
    """
    dataset_name = "DS " + random_lower_string()
    dataset_description = "DS desc " + random_lower_string()
    return DatasetCreate(name=dataset_name, description=dataset_description,
                         hours_per_time_step=1, number_of_time_steps=8760,
                         cost_unit='1e9 Euro', length_unit='km',
                         ref_created_by=1)


def random_existing_dataset(db: Session) -> Dataset:
    """
    Generates a random existing dataset.
    """
    user = crud.user.get(db=db, id=1)
    if user is None:
        create_random_user(db=db)
    create_request = random_dataset_create()
    return crud.dataset.create(db=db, obj_in=create_request)


def fixed_dataset_create() -> DatasetCreate:
    """
    Generates a fixed dataset create request.
    Will always return the same create request.
    """
    return DatasetCreate(name="Fixed dataset", description="Fixed dataset description", ref_created_by=1)


def fixed_existing_dataset(db: Session) -> Dataset:
    """
    Generates a fixed existing dataset.
    Will always return the same dataset.
    """
    user = crud.user.get(db=db, id=1)
    if user is None:
        create_random_user(db=db)
    create_request = fixed_dataset_create()
    dataset = crud.dataset.get_by_name(db=db, name=create_request.name)
    if dataset is None:
        dataset = crud.dataset.create(db=db, obj_in=create_request)
    return dataset
