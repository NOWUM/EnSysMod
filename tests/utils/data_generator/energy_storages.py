from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyCommodity, EnergyStorage
from ensysmod.schemas import EnergyStorageCreate
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.utils import random_string


def storage_create_request(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergyStorageCreate:
    """
    Generate a storage create request with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header).id
    if commodity is None:
        commodity = new_commodity(db, user_header, dataset_id=dataset_id)
    return EnergyStorageCreate(
        ref_dataset=dataset_id,
        name=f"EnergyStorage-Dataset{dataset_id}-{random_string()}",
        description=None,
        commodity_name=commodity.name,
        charge_efficiency=0.9,
        discharge_efficiency=0.9,
        cyclic_lifetime=100_000,
        charge_rate=1,
        discharge_rate=1,
        self_discharge=1 - (1 - 0.03) ** (1 / (30 * 24)),
        state_of_charge_min=0.33,
        state_of_charge_max=0.66,
    )


def new_storage(
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    commodity: EnergyCommodity | None = None,
) -> EnergyStorage:
    """
    Create a storage component with the specified dataset and commodity.
    If dataset_id or commodity is not specified, it will be generated.
    """
    create_request = storage_create_request(db, user_header, dataset_id=dataset_id, commodity=commodity)
    return crud.energy_storage.create(db=db, obj_in=create_request)
