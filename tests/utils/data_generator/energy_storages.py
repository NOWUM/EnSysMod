from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyStorage
from ensysmod.schemas import EnergyStorageCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.utils import random_lower_string


def storage_create_request(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyStorageCreate:
    """
    Generate a storage create request with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    if commodity_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id).name
    return EnergyStorageCreate(
        ref_dataset=dataset_id,
        name=f"EnergyStorage-Dataset{dataset_id}-{random_lower_string()}",
        description="Description",
        commodity=commodity_name,
        charge_efficiency=0.9,
        discharge_efficiency=0.9,
        cyclic_lifetime=100_000,
        charge_rate=1,
        discharge_rate=1,
        self_discharge=1 - (1 - 0.03) ** (1 / (30 * 24)),
        stateOfChargeMin=0.33,
        stateOfChargeMax=0.66,
    )


def storage_create(
    db: Session,
    current_user_header: dict[str, str],
    dataset_id: int | None = None,
    commodity_name: str | None = None,
) -> EnergyStorage:
    """
    Create a storage component with the specified dataset and commodity.
    If dataset_id or commodity_name is not specified, it will be generated.
    """
    create_request = storage_create_request(db, current_user_header, dataset_id, commodity_name)
    return crud.energy_storage.create(db=db, obj_in=create_request)
