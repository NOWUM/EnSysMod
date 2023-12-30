from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity
from ensysmod.schemas import EnergyCommodityCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.utils import random_lower_string


def commodity_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyCommodityCreate:
    """
    Generate a commodity create request with the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    return EnergyCommodityCreate(
        name=f"EnergyCommodity-Dataset{dataset_id}-{random_lower_string()}",
        unit="kWh",
        description="EnergyCommodity description",
        ref_dataset=dataset_id,
    )


def commodity_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
) -> EnergyCommodity:
    """
    Create a commodity in the specified dataset.
    If dataset_id is not specified, it will be generated.
    """
    create_request = commodity_create_request(db, current_user_header, dataset_id)
    return crud.energy_commodity.create(db=db, obj_in=create_request)
