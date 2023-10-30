from sqlalchemy.orm import Session

from ensysmod.schemas import OperationRateFixCreate, OperationRateMaxCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_float_numbers


def operation_rate_fix_create_request(db: Session, current_user_header: dict[str, str]) -> OperationRateFixCreate:
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    component = source_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    region = region_create(db, current_user_header, dataset_id=dataset.id)
    return OperationRateFixCreate(
        ref_dataset=dataset.id,
        component=component.component.name,
        region=region.name,
        fix_operation_rates=random_float_numbers(8760)
    )


def operation_rate_max_create_request(db: Session, current_user_header: dict[str, str]) -> OperationRateMaxCreate:
    dataset = dataset_create(db, current_user_header)
    commodity = commodity_create(db, current_user_header, dataset_id=dataset.id)
    component = source_create(db, current_user_header, dataset_id=dataset.id, commodity_name=commodity.name)
    region = region_create(db, current_user_header, dataset_id=dataset.id)
    return OperationRateMaxCreate(
        ref_dataset=dataset.id,
        component=component.component.name,
        region=region.name,
        max_operation_rates=random_float_numbers(8760)
    )
