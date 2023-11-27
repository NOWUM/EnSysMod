from pathlib import Path
from tempfile import mkstemp
from typing import Literal

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import OperationRateFixCreate, OperationRateMaxCreate
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_float_number

_operation_rate_types = Literal["fix", "max"]


def operation_rate_create_request(
    type: _operation_rate_types,
    db: Session,
    current_user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    component_name: str | None = None,
    region_name: str | None = None,
    length: int = 8760,
) -> OperationRateFixCreate | OperationRateMaxCreate:
    """
    Generate an operation rate create request of the specified type with the specified dataset_id, component_name, region_name and length.
    If parameters are not specified, it will be generated.
    """
    if dataset_id is None:
        dataset_id = dataset_create(db, current_user_header).id
    if component_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id=dataset_id).name
        component_name = source_create(db, current_user_header, dataset_id=dataset_id, commodity_name=commodity_name).component.name
    if region_name is None:
        region_name = region_create(db, current_user_header, dataset_id=dataset_id).name

    if type == "max":
        return OperationRateMaxCreate(
            ref_dataset=dataset_id,
            component=component_name,
            region=region_name,
            region_to=None,
            max_operation_rates=random_float_number(size=length),
        )
    return OperationRateFixCreate(
        ref_dataset=dataset_id,
        component=component_name,
        region=region_name,
        region_to=None,
        fix_operation_rates=random_float_number(size=length),
    )


def operation_rate_create(
    type: _operation_rate_types,
    db: Session,
    current_user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    component_name: str | None = None,
    region_name: str | None = None,
    length: int = 8760,
):
    """
    Create an operation rate of the specified type with the specified dataset_id, component_name, region_name and length.
    If parameters are not specified, it will be generated.
    """
    create_request = operation_rate_create_request(
        type=type,
        db=db,
        current_user_header=current_user_header,
        dataset_id=dataset_id,
        component_name=component_name,
        region_name=region_name,
        length=length,
    )
    if type == "max":
        return crud.operation_rate_max.create(db=db, obj_in=create_request)
    return crud.operation_rate_fix.create(db=db, obj_in=create_request)


def generate_time_series_excel_file(region_names: list[str], length: int = 8760) -> Path:
    data_dict: dict[str, list[float]] = {}
    for region_name in region_names:
        data_dict[region_name] = random_float_number(size=length)

    _, temp_file_path = mkstemp(prefix="ensysmod_time_series_", suffix=".xlsx")
    pd.DataFrame(data_dict).to_excel(temp_file_path)
    return Path(temp_file_path)
