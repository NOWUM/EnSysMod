from enum import Enum
from typing import NamedTuple

from pydantic import BaseModel

from ensysmod import crud, schemas
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix


class FolderTypeEnum(Enum):
    CONVERSION = "conversion"
    SINK = "sink"
    SOURCE = "source"
    STORAGE = "storage"
    TRANSMISSION = "transmission"


class FileTypeEnum(Enum):
    REGIONS = "regions"
    COMMODITIES = "commodities"
    OPERATION_RATE_FIX = "operationRateFix"
    OPERATION_RATE_MAX = "operationRateMax"
    CAPACITY_FIX = "capacityFix"
    CAPACITY_MAX = "capacityMax"
    CAPACITY_MIN = "capacityMin"
    YEARLY_FULL_LOAD_HOURS_MAX = "yearlyFullLoadHoursMax"
    YEARLY_FULL_LOAD_HOURS_MIN = "yearlyFullLoadHoursMin"
    DISTANCES = "distances"
    LOSS = "loss"


class FolderType(NamedTuple):
    folder_type: str
    crud_repo: CRUDBaseDependsComponent
    create_schema: type[BaseModel]
    as_matrix: bool = False


class FileType(NamedTuple):
    file_name: str
    crud_repo: CRUDBaseDependsDataset
    create_schema: type[BaseModel]


class ExcelFileType(NamedTuple):
    file_name: str
    crud_repo: CRUDBaseDependsMatrix
    create_schema: type[BaseModel]
    as_list: bool = False


conversion = FolderType(
    folder_type=FolderTypeEnum.CONVERSION.value,
    crud_repo=crud.energy_conversion,
    create_schema=schemas.EnergyConversionCreate,
)

sink = FolderType(
    folder_type=FolderTypeEnum.SINK.value,
    crud_repo=crud.energy_sink,
    create_schema=schemas.EnergySinkCreate,
)

source = FolderType(
    folder_type=FolderTypeEnum.SOURCE.value,
    crud_repo=crud.energy_source,
    create_schema=schemas.EnergySourceCreate,
)

storage = FolderType(
    folder_type=FolderTypeEnum.STORAGE.value,
    crud_repo=crud.energy_storage,
    create_schema=schemas.EnergyStorageCreate,
)

transmission = FolderType(
    folder_type=FolderTypeEnum.TRANSMISSION.value,
    crud_repo=crud.energy_transmission,
    create_schema=schemas.EnergyTransmissionCreate,
    as_matrix=True,
)

regions = FileType(
    file_name=FileTypeEnum.REGIONS.value,
    crud_repo=crud.region,
    create_schema=schemas.RegionCreate,
)

commodities = FileType(
    file_name=FileTypeEnum.COMMODITIES.value,
    crud_repo=crud.energy_commodity,
    create_schema=schemas.EnergyCommodityCreate,
)

operation_rate_fix = ExcelFileType(
    file_name=FileTypeEnum.OPERATION_RATE_FIX.value,
    crud_repo=crud.operation_rate_fix,
    create_schema=schemas.OperationRateFixCreate,
    as_list=True,
)

operation_rate_max = ExcelFileType(
    file_name=FileTypeEnum.OPERATION_RATE_MAX.value,
    crud_repo=crud.operation_rate_max,
    create_schema=schemas.OperationRateMaxCreate,
    as_list=True,
)

capacity_fix = ExcelFileType(
    file_name=FileTypeEnum.CAPACITY_FIX.value,
    crud_repo=crud.capacity_fix,
    create_schema=schemas.CapacityFixCreate,
)

capacity_max = ExcelFileType(
    file_name=FileTypeEnum.CAPACITY_MAX.value,
    crud_repo=crud.capacity_max,
    create_schema=schemas.CapacityMaxCreate,
)

capacity_min = ExcelFileType(
    file_name=FileTypeEnum.CAPACITY_MIN.value,
    crud_repo=crud.capacity_min,
    create_schema=schemas.CapacityMinCreate,
)

yearly_full_load_hours_max = ExcelFileType(
    file_name=FileTypeEnum.YEARLY_FULL_LOAD_HOURS_MAX.value,
    crud_repo=crud.yearly_full_load_hour_max,
    create_schema=schemas.YearlyFullLoadHourMaxCreate,
)

yearly_full_load_hours_min = ExcelFileType(
    file_name=FileTypeEnum.YEARLY_FULL_LOAD_HOURS_MIN.value,
    crud_repo=crud.yearly_full_load_hour_min,
    create_schema=schemas.YearlyFullLoadHourMinCreate,
)

distances = ExcelFileType(
    file_name=FileTypeEnum.DISTANCES.value,
    crud_repo=crud.energy_transmission_distance,
    create_schema=schemas.EnergyTransmissionDistanceCreate,
)

loss = ExcelFileType(
    file_name=FileTypeEnum.LOSS.value,
    crud_repo=crud.energy_transmission_loss,
    create_schema=schemas.EnergyTransmissionLossCreate,
)


folder_types: tuple[FolderType, ...] = (conversion, sink, source, storage, transmission)
json_list_file_types: tuple[FileType, ...] = (regions, commodities)
excel_file_types: tuple[ExcelFileType, ...] = (
    operation_rate_fix,
    operation_rate_max,
    capacity_fix,
    capacity_max,
    capacity_min,
    yearly_full_load_hours_max,
    yearly_full_load_hours_min,
    distances,
    loss,
)
