from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergySource
from ensysmod.schemas import EnergySourceCreate
from tests.utils.data_generator import fixed_existing_dataset, fixed_existing_energy_commodity
from tests.utils.utils import random_lower_string


def random_energy_source_create(db: Session) -> EnergySourceCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergySourceCreate(
        ref_dataset=dataset.id,
        name=f"EnergySource-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
        commodity_cost=42.3
    )


def random_existing_energy_source(db: Session) -> EnergySource:
    create_request = random_energy_source_create(db)
    return crud.energy_source.create(db=db, obj_in=create_request)


def fixed_energy_source_create(db: Session) -> EnergySourceCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergySourceCreate(
        ref_dataset=dataset.id,
        name=f"EnergySource-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
    )


def fixed_existing_energy_source(db: Session) -> EnergySource:
    create_request = fixed_energy_source_create(db)
    source = crud.energy_source.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset,
                                                        name=create_request.name)
    if source is None:
        source = crud.energy_source.create(db=db, obj_in=create_request)
    return source
