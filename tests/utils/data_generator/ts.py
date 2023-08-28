from sqlalchemy.orm import Session

from ensysmod.schemas import (
    CapacityFixCreate,
    CapacityMaxCreate,
    CapacityMinCreate,
    OperationRateFixCreate,
    OperationRateMaxCreate,
)
from tests.utils import data_generator
from tests.utils.utils import random_float_numbers


def get_random_fix_capacity_create(db: Session) -> CapacityFixCreate:
    source = data_generator.fixed_existing_energy_sink(db)
    region = data_generator.fixed_existing_region(db)
    return CapacityFixCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        fix_capacities=random_float_numbers(8760)
    )


def get_random_max_capacity_create(db: Session) -> CapacityMaxCreate:
    source = data_generator.fixed_existing_energy_sink(db)
    region = data_generator.fixed_existing_region(db)
    return CapacityMaxCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        max_capacities=random_float_numbers(8760)
    )


def get_random_min_capacity_create(db: Session) -> CapacityMinCreate:
    source = data_generator.fixed_existing_energy_sink(db)
    region = data_generator.fixed_existing_region(db)
    return CapacityMinCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        min_capacities=random_float_numbers(8760)
    )


def get_random_fix_operation_rate_create(db: Session) -> OperationRateFixCreate:
    source = data_generator.fixed_existing_energy_sink(db)
    region = data_generator.fixed_existing_region(db)
    return OperationRateFixCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        fix_operation_rates=random_float_numbers(8760)
    )


def get_random_max_operation_rate_create(db: Session) -> OperationRateMaxCreate:
    source = data_generator.fixed_existing_energy_sink(db)
    region = data_generator.fixed_existing_region(db)
    return OperationRateMaxCreate(
        ref_dataset=region.ref_dataset,
        component=source.component.name,
        region=region.name,
        max_operation_rates=random_float_numbers(8760)
    )
