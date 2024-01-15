from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyTransmission
from ensysmod.schemas import EnergyTransmissionCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.utils import random_string


def transmission_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyTransmissionCreate:
    """
    Generate a transmission create request with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    if commodity_name is None:
        commodity_name = new_commodity(db, user_header, dataset_id=dataset_id).name
    return EnergyTransmissionCreate(
        ref_dataset=dataset_id,
        name=f"EnergyTransmission-Dataset{dataset_id}-{random_string()}",
        description=None,
        commodity=commodity_name,
    )


def new_transmission(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyTransmission:
    """
    Create a transmission component with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    create_request = transmission_create_request(db, user_header, dataset_id=dataset_id, commodity_name=commodity_name)
    return crud.energy_transmission.create(db=db, obj_in=create_request)
