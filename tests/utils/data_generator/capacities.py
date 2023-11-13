from typing import Literal

from sqlalchemy.orm import Session

from ensysmod.schemas import CapacityFixCreate, CapacityMaxCreate, CapacityMinCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.energy_transmissions import transmission_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_float_number

_capacity_types = Literal["fix", "max", "min"]


def capacity_create_request(
    type: _capacity_types,
    db: Session,
    current_user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    component_name: str | None = None,
    region_name: str | None = None,
    transmission_component: bool = False,
    region_to_name: str | None = None,
) -> CapacityFixCreate | CapacityMaxCreate | CapacityMinCreate:
    """
    Generate a capacity create request of the specified type with the specified dataset_id, component_name, region_name and region_to_name.
    If parameters are not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    if component_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id=dataset_id).name
        component_name = (
            transmission_create(db, current_user_header, dataset_id=dataset_id, commodity_name=commodity_name).component.name
            if transmission_component
            else source_create(db, current_user_header, dataset_id=dataset_id, commodity_name=commodity_name).component.name
        )
    if region_name is None:
        region_name = region_create(db, current_user_header, dataset_id=dataset_id).name
    if region_to_name is None and transmission_component is True:
        region_to_name = region_create(db, current_user_header, dataset_id=dataset_id).name

    if type == "max":
        return CapacityMaxCreate(
            ref_dataset=dataset_id,
            component=component_name,
            region=region_name,
            region_to=region_to_name,
            max_capacity=random_float_number(),
        )
    if type == "min":
        return CapacityMinCreate(
            ref_dataset=dataset_id,
            component=component_name,
            region=region_name,
            region_to=region_to_name,
            min_capacity=random_float_number(),
        )
    return CapacityFixCreate(
        ref_dataset=dataset_id,
        component=component_name,
        region=region_name,
        region_to=region_to_name,
        fix_capacity=random_float_number(),
    )
