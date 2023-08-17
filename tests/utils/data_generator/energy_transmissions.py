from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyTransmission
from ensysmod.schemas import EnergyTransmissionCreate
from tests.utils.data_generator import (
    fixed_existing_dataset,
    fixed_existing_energy_commodity,
)
from tests.utils.utils import random_lower_string


def random_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
    )


def random_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = random_energy_transmission_create(db)
    return crud.energy_transmission.create(db=db, obj_in=create_request)


def fixed_energy_transmission_create(db: Session) -> EnergyTransmissionCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergyTransmissionCreate(
        ref_dataset=dataset.id,
        name=f"EnergyTransmission-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
    )


def fixed_existing_energy_transmission(db: Session) -> EnergyTransmission:
    create_request = fixed_energy_transmission_create(db)
    transmission = crud.energy_transmission.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset, name=create_request.name)
    if transmission is None:
        transmission = crud.energy_transmission.create(db=db, obj_in=create_request)
    return transmission
