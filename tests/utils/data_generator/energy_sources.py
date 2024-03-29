from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity, EnergySource
from ensysmod.schemas import EnergySourceCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.utils import random_string


def source_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergySourceCreate:
    """
    Generate a source create request with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    if commodity is None:
        commodity = new_commodity(db, user_header, dataset_id=dataset_id)
    return EnergySourceCreate(
        ref_dataset=dataset_id,
        name=f"EnergySource-Dataset{dataset_id}-{random_string()}",
        description=None,
        commodity_name=commodity.name,
        commodity_cost=42.3,
    )


def new_source(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergySource:
    """
    Create a source component with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    create_request = source_create_request(db, user_header, dataset_id=dataset_id, commodity=commodity)
    return crud.energy_source.create(db=db, obj_in=create_request)
