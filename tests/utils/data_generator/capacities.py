from sqlalchemy.orm import Session

from ensysmod.schemas import CapacityFixCreate, CapacityMaxCreate, CapacityMinCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_float_numbers


def capacity_fix_create_request(db: Session, current_user_header: dict[str, str]) -> CapacityFixCreate:
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    component = source_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    region = region_create(db, current_user_header, dataset_id=dataset.id)
    return CapacityFixCreate(
        ref_dataset=dataset.id,
        component=component.component.name,
        region=region.name,
        fix_capacities=random_float_numbers(8760)
    )


def capacity_max_create_request(db: Session, current_user_header: dict[str, str]) -> CapacityMaxCreate:
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    component = source_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    region = region_create(db, current_user_header, dataset_id=dataset.id)
    return CapacityMaxCreate(
        ref_dataset=dataset.id,
        component=component.component.name,
        region=region.name,
        max_capacities=random_float_numbers(8760)
    )


def capacity_min_create_request(db: Session, current_user_header: dict[str, str]) -> CapacityMinCreate:
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    component = source_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    region = region_create(db, current_user_header, dataset_id=dataset.id)
    return CapacityMinCreate(
        ref_dataset=dataset.id,
        component=component.component.name,
        region=region.name,
        min_capacities=random_float_numbers(8760)
    )
