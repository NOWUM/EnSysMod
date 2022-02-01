from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergySink
from ensysmod.schemas import EnergySinkCreate
from tests.utils.data_generator.datasets import fixed_existing_dataset
from tests.utils.data_generator.energy_commodities import fixed_existing_energy_commodity
from tests.utils.utils import random_lower_string


def random_energy_sink_create(db: Session) -> EnergySinkCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergySinkCreate(
        ref_dataset=dataset.id,
        name=f"EnergySink-{dataset.id}-{random_lower_string()}",
        description="Description",
        commodity=commodity.name,
        yearly_limit=1000,
    )


def random_existing_energy_sink(db: Session) -> EnergySink:
    create_request = random_energy_sink_create(db)
    return crud.energy_sink.create(db=db, obj_in=create_request)


def fixed_energy_sink_create(db: Session) -> EnergySinkCreate:
    dataset = fixed_existing_dataset(db)
    commodity = fixed_existing_energy_commodity(db)
    return EnergySinkCreate(
        ref_dataset=dataset.id,
        name=f"EnergySink-{dataset.id}-Fixed",
        description="Description",
        commodity=commodity.name,
    )


def fixed_existing_energy_sink(db: Session) -> EnergySink:
    create_request = fixed_energy_sink_create(db)
    sink = crud.energy_sink.get_by_dataset_and_name(db=db, dataset_id=create_request.ref_dataset,
                                                    name=create_request.name)
    if sink is None:
        sink = crud.energy_sink.create(db=db, obj_in=create_request)
    return sink
