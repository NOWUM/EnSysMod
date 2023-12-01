from pathlib import Path
from tempfile import mkstemp

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod.core.file_folder_types import ExcelFileType
from tests.utils.data_generator.datasets import dataset_create
from tests.utils.data_generator.energy_commodities import commodity_create
from tests.utils.data_generator.energy_sources import source_create
from tests.utils.data_generator.energy_transmissions import transmission_create
from tests.utils.data_generator.regions import region_create
from tests.utils.utils import random_float_number


def excel_file_type_create_request(
    excel_file_type: ExcelFileType,
    db: Session,
    current_user_header: dict[str, str],
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
        dataset_id = dataset_create(db, current_user_header, number_of_time_steps=number_of_time_steps).id
    if component_name is None:
        commodity_name = commodity_create(db, current_user_header, dataset_id=dataset_id).name
        if transmission_component:
            component_name = transmission_create(db, current_user_header, dataset_id=dataset_id, commodity_name=commodity_name).component.name
        else:
            component_name = source_create(db, current_user_header, dataset_id=dataset_id, commodity_name=commodity_name).component.name
    if region_name is None:
        region_name = region_create(db, current_user_header, dataset_id=dataset_id).name
    if transmission_component and region_to_name is None:
        region_to_name = region_create(db, current_user_header, dataset_id=dataset_id).name

    data_column = {
        excel_file_type.data_column: random_float_number(size=number_of_time_steps) if excel_file_type.as_list else random_float_number(),
    }

    return excel_file_type.create_schema(
        ref_dataset=dataset_id,
        component=component_name,
        region=region_name,
        region_to=region_to_name,
        **data_column,
    )


def excel_file_type_create(
    excel_file_type: ExcelFileType,
    db: Session,
    current_user_header: dict[str, str],
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
        current_user_header=current_user_header,
        dataset_id=dataset_id,
        component_name=component_name,
        region_name=region_name,
        region_to_name=region_to_name,
        transmission_component=transmission_component,
        number_of_time_steps=number_of_time_steps,
    )
    return excel_file_type.crud_repo.create(db=db, obj_in=create_request)


def generate_time_series_excel_file(region_names: list[str], length: int = 8760) -> Path:
    size = (length, len(region_names))
    _, temp_file_path = mkstemp(prefix="ensysmod_time_series_", suffix=".xlsx")
    pd.DataFrame(random_float_number(size=size), columns=region_names).to_excel(temp_file_path)
    return Path(temp_file_path)


def generate_array_excel_file(region_names: list[str]) -> Path:
    size = (1, len(region_names))
    _, temp_file_path = mkstemp(prefix="ensysmod_array_", suffix=".xlsx")
    pd.DataFrame(random_float_number(size=size), columns=region_names).to_excel(temp_file_path)
    return Path(temp_file_path)


def generate_matrix_excel_file(region_names: list[str]) -> Path:
    size = (len(region_names), len(region_names))
    _, temp_file_path = mkstemp(prefix="ensysmod_matrix_", suffix=".xlsx")
    pd.DataFrame(random_float_number(size=size), columns=region_names, index=region_names).to_excel(temp_file_path)
    return Path(temp_file_path)
