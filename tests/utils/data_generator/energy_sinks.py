from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity, EnergySink
from ensysmod.schemas import EnergySinkCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.utils import random_string


def sink_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergySinkCreate:
    """
    Generate a sink create request with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    if commodity is None:
        commodity = new_commodity(db, user_header, dataset_id=dataset_id)
    return EnergySinkCreate(
        ref_dataset=dataset_id,
        name=f"EnergySink-Dataset{dataset_id}-{random_string()}",
        description=None,
        commodity=commodity.name,
        yearly_limit=1000,
        commodity_limit_id="limit_id",
        commodity_cost=999,
    )


def new_sink(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergySink:
    """
    Create a sink component with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    create_request = sink_create_request(db, user_header, dataset_id=dataset_id, commodity=commodity)
    return crud.energy_sink.create(db=db, obj_in=create_request)
