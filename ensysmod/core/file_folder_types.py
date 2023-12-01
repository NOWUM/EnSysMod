from typing import NamedTuple

from pydantic import BaseModel

from ensysmod import crud, schemas
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix


class FolderType(NamedTuple):
    folder_name: str
    file_name: str
    crud_repo: CRUDBaseDependsComponent
    create_schema: type[BaseModel]
    as_matrix: bool = False


class JsonFileType(NamedTuple):
    file_name: str
    crud_repo: CRUDBaseDependsDataset
    create_schema: type[BaseModel]


class ExcelFileType(NamedTuple):
    file_name: str
    crud_repo: CRUDBaseDependsMatrix
    create_schema: type[BaseModel]
    data_column: str
    as_list: bool = False


CONVERSION = FolderType(
    folder_name="conversions",
    file_name="conversion.json",
    crud_repo=crud.energy_conversion,
    create_schema=schemas.EnergyConversionCreate,
)

SINK = FolderType(
    folder_name="sinks",
    file_name="sink.json",
    crud_repo=crud.energy_sink,
    create_schema=schemas.EnergySinkCreate,
)

SOURCE = FolderType(
    folder_name="sources",
    file_name="source.json",
    crud_repo=crud.energy_source,
    create_schema=schemas.EnergySourceCreate,
)

STORAGE = FolderType(
    folder_name="storages",
    file_name="storage.json",
    crud_repo=crud.energy_storage,
    create_schema=schemas.EnergyStorageCreate,
)

TRANSMISSION = FolderType(
    folder_name="transmissions",
    file_name="transmission.json",
    crud_repo=crud.energy_transmission,
    create_schema=schemas.EnergyTransmissionCreate,
    as_matrix=True,
)

REGIONS = JsonFileType(
    file_name="regions.json",
    crud_repo=crud.region,
    create_schema=schemas.RegionCreate,
)

COMMODITIES = JsonFileType(
    file_name="commodities.json",
    crud_repo=crud.energy_commodity,
    create_schema=schemas.EnergyCommodityCreate,
)

OPERATION_RATE_FIX = ExcelFileType(
    file_name="operationRateFix.xlsx",
    crud_repo=crud.operation_rate_fix,
    create_schema=schemas.OperationRateFixCreate,
    data_column="fix_operation_rates",
    as_list=True,
)

OPERATION_RATE_MAX = ExcelFileType(
    file_name="operationRateMax.xlsx",
    crud_repo=crud.operation_rate_max,
    create_schema=schemas.OperationRateMaxCreate,
    data_column="max_operation_rates",
    as_list=True,
)

CAPACITY_FIX = ExcelFileType(
    file_name="capacityFix.xlsx",
    crud_repo=crud.capacity_fix,
    create_schema=schemas.CapacityFixCreate,
    data_column="fix_capacity",
)

CAPACITY_MAX = ExcelFileType(
    file_name="capacityMax.xlsx",
    crud_repo=crud.capacity_max,
    create_schema=schemas.CapacityMaxCreate,
    data_column="max_capacity",
)

CAPACITY_MIN = ExcelFileType(
    file_name="capacityMin.xlsx",
    crud_repo=crud.capacity_min,
    create_schema=schemas.CapacityMinCreate,
    data_column="min_capacity",
)

YEARLY_FULL_LOAD_HOURS_MAX = ExcelFileType(
    file_name="yearlyFullLoadHoursMax.xlsx",
    crud_repo=crud.yearly_full_load_hour_max,
    create_schema=schemas.YearlyFullLoadHourMaxCreate,
    data_column="max_yearly_full_load_hour",
)

YEARLY_FULL_LOAD_HOURS_MIN = ExcelFileType(
    file_name="yearlyFullLoadHoursMin.xlsx",
    crud_repo=crud.yearly_full_load_hour_min,
    create_schema=schemas.YearlyFullLoadHourMinCreate,
    data_column="min_yearly_full_load_hour",
)

DISTANCES = ExcelFileType(
    file_name="distances.xlsx",
    crud_repo=crud.energy_transmission_distance,
    create_schema=schemas.EnergyTransmissionDistanceCreate,
    data_column="distance",
)

LOSSES = ExcelFileType(
    file_name="losses.xlsx",
    crud_repo=crud.energy_transmission_loss,
    create_schema=schemas.EnergyTransmissionLossCreate,
    data_column="loss",
)


FOLDER_TYPES: tuple[FolderType, ...] = (
    CONVERSION,
    SINK,
    SOURCE,
    STORAGE,
    TRANSMISSION,
)
JSON_FILE_TYPES: tuple[JsonFileType, ...] = (
    REGIONS,
    COMMODITIES,
)
EXCEL_FILE_TYPES: tuple[ExcelFileType, ...] = (
    OPERATION_RATE_FIX,
    OPERATION_RATE_MAX,
    CAPACITY_FIX,
    CAPACITY_MAX,
    CAPACITY_MIN,
    YEARLY_FULL_LOAD_HOURS_MAX,
    YEARLY_FULL_LOAD_HOURS_MIN,
    DISTANCES,
    LOSSES,
)
