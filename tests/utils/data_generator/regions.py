from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.utils import random_string


def region_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
) -> RegionCreate:
    """
    Generate a region create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    return RegionCreate(
        name=f"Region-Dataset{dataset_id}-{random_string()}",
        ref_dataset=dataset_id,
    )


def new_region(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
) -> Region:
    """
    Create a region in the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = region_create_request(db, user_header, dataset_id=dataset_id)
    return crud.region.create(db=db, obj_in=create_request)
