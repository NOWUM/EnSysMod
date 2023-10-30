from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.utils import random_lower_string


def region_create_request(db: Session, current_user_header: dict[str, str], dataset_id: int | None = None) -> RegionCreate:
    """
    Generate a region create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    return RegionCreate(
        name=f"Region-Dataset{dataset_id}-{random_lower_string()}",
        ref_dataset=dataset_id,
    )


def region_create(db: Session, current_user_header: dict[str, str], dataset_id: int | None = None) -> Region:
    """
    Create a region in the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = region_create_request(db, current_user_header, dataset_id)
    return crud.region.create(db=db, obj_in=create_request)
