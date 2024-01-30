from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import ExcelFileType
from ensysmod.utils.utils import create_temp_file, remove_file
from tests.utils.data_generator.datasets import new_dataset
from tests.utils.data_generator.energy_commodities import new_commodity
from tests.utils.data_generator.energy_sources import new_source
from tests.utils.data_generator.energy_transmissions import new_transmission
from tests.utils.data_generator.regions import new_region
from tests.utils.utils import random_float_number


def excel_file_type_create_request(
    excel_file_type: ExcelFileType,
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    component_name: str | None = None,
    transmission_component: bool = False,
    region_name: str | None = None,
    region_to_name: str | None = None,
    number_of_time_steps: int = 8760,
):
    """
    Generate an excel file type create request with the specified dataset_id, component_name, region_name, region_to_name and number_of_time_steps.
    If parameters are not specified, it will be generated, except for region_to, which will only be generated if transmission_component is True.
    """
    if dataset_id is None:
        dataset_id = new_dataset(db, user_header, number_of_time_steps=number_of_time_steps).id
    if component_name is None:
        commodity = new_commodity(db, user_header, dataset_id=dataset_id)
        if transmission_component:
            component_name = new_transmission(db, user_header, dataset_id=dataset_id, commodity=commodity).component.name
        else:
            component_name = new_source(db, user_header, dataset_id=dataset_id, commodity=commodity).component.name
    if region_name is None:
        region_name = new_region(db, user_header, dataset_id=dataset_id).name
    if region_to_name is None and transmission_component:
        region_to_name = new_region(db, user_header, dataset_id=dataset_id).name

    data_column = {excel_file_type.data_column: random_float_number(size=number_of_time_steps) if excel_file_type.as_list else random_float_number()}

    return excel_file_type.create_schema(
        ref_dataset=dataset_id,
        component=component_name,
        region=region_name,
        region_to=region_to_name,
        **data_column,
    )


def new_excel_file_type(
    excel_file_type: ExcelFileType,
    db: Session,
    user_header: dict[str, str],
    *,
    dataset_id: int | None = None,
    component_name: str | None = None,
    transmission_component: bool = False,
    region_name: str | None = None,
    region_to_name: str | None = None,
    number_of_time_steps: int = 8760,
):
    """
    Create an excel file type with the specified dataset_id, component_name, region_name, region_to_name and number_of_time_steps.
    If parameters are not specified, it will be generated, except for region_to, which will only be generated if transmission_component is True.
    """
    create_request = excel_file_type_create_request(
        excel_file_type=excel_file_type,
        db=db,
        user_header=user_header,
        dataset_id=dataset_id,
        component_name=component_name,
        region_name=region_name,
        region_to_name=region_to_name,
        transmission_component=transmission_component,
        number_of_time_steps=number_of_time_steps,
    )
    return excel_file_type.crud_repo.create(db=db, obj_in=create_request)


@contextmanager
def generate_excel_file(*, region_names: list[str], length: int = 8760, as_matrix: bool = False) -> Generator[Path, None, None]:
    temp_file_path = create_temp_file(prefix="ensysmod_", suffix=".xlsx")
    if as_matrix:
        size = (len(region_names), len(region_names))
        pd.DataFrame(random_float_number(size=size), columns=region_names, index=region_names).to_excel(temp_file_path)
    else:
        size = (length, len(region_names))
        pd.DataFrame(random_float_number(size=size), columns=region_names).to_excel(temp_file_path)
    try:
        yield temp_file_path
    finally:
        remove_file(temp_file_path)
