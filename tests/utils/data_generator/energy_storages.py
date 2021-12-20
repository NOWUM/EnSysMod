from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyStorage
from ensysmod.schemas import EnergyStorageCreate
from tests.utils.data_generator import fixed_existing_dataset, fixed_existing_energy_commodity
from tests.utils.utils import random_lower_string


def random_energy_storage_create(db: Session) -> EnergyStorageCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyStorageCreate(
        ref_dataset=dataset.id,
        name=f"EnergyStorage-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
        charge_efficiency=0.9,
        discharge_efficiency=0.9,
        cyclic_lifetime=100_000,
        charge_rate=1,
        discharge_rate=1,
        self_discharge=1 - (1 - 0.03) ** (1 / (30 * 24)),
        stateOfChargeMin=0.33,
        stateOfChargeMax=0.66,
    )


def random_existing_energy_storage(db: Session) -> EnergyStorage:
    create_request = random_energy_storage_create(db)
    return crud.energy_storage.create(db=db, obj_in=create_request)


def fixed_energy_storage_create(db: Session) -> EnergyStorageCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyStorageCreate(
        ref_dataset=dataset.id,
        name=f"EnergyStorage-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
    )


def fixed_existing_energy_storage(db: Session) -> EnergyStorage:
    create_request = fixed_energy_storage_create(db)
    storage = crud.energy_storage.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset,
                                                          name=create_request.name)
    if storage is None:
        storage = crud.energy_storage.create(db=db, obj_in=create_request)
    return storage
