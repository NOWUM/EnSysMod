"""
This package contains every model that is returned from the Rest-API.
"""
from .dataset import Dataset, DatasetCreate, DatasetUpdate
from .dataset_permission import (
    DatasetPermission,
    DatasetPermissionCreate,
    DatasetPermissionUpdate,
)
from .energy_commodity import (
    EnergyCommodity,
    EnergyCommodityCreate,
    EnergyCommodityUpdate,
)
from .energy_component import (
    EnergyComponent,
    EnergyComponentCreate,
    EnergyComponentUpdate,
)
from .energy_conversion import (
    EnergyConversion,
    EnergyConversionCreate,
    EnergyConversionUpdate,
)
from .energy_conversion_factor import (
    EnergyConversionFactor,
    EnergyConversionFactorCreate,
    EnergyConversionFactorUpdate,
)
from .energy_model import EnergyModel, EnergyModelCreate, EnergyModelUpdate
from .energy_model_optimization import (
    EnergyModelOptimization,
    EnergyModelOptimizationCreate,
    EnergyModelOptimizationUpdate,
)
from .energy_model_override import (
    EnergyModelOverride,
    EnergyModelOverrideCreate,
    EnergyModelOverrideUpdate,
)
from .energy_sink import EnergySink, EnergySinkCreate, EnergySinkUpdate
from .energy_source import EnergySource, EnergySourceCreate, EnergySourceUpdate
from .energy_storage import EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate
from .energy_transmission import (
    EnergyTransmission,
    EnergyTransmissionCreate,
    EnergyTransmissionUpdate,
)
from .energy_transmission_distance import (
    EnergyTransmissionDistance,
    EnergyTransmissionDistanceCreate,
    EnergyTransmissionDistanceUpdate,
)
from .energy_transmission_loss import (
    EnergyTransmissionLoss,
    EnergyTransmissionLossCreate,
    EnergyTransmissionLossUpdate,
)
from .file_upload import FileStatus, FileUploadResult, ZipArchiveUploadResult
from .region import Region, RegionCreate, RegionUpdate
from .token import Token, TokenPayload
from .ts_capacity_fix import CapacityFix, CapacityFixCreate, CapacityFixUpdate
from .ts_capacity_max import CapacityMax, CapacityMaxCreate, CapacityMaxUpdate
from .ts_capacity_min import CapacityMin, CapacityMinCreate, CapacityMinUpdate
from .ts_operation_rate_fix import (
    OperationRateFix,
    OperationRateFixCreate,
    OperationRateFixUpdate,
)
from .ts_operation_rate_max import (
    OperationRateMax,
    OperationRateMaxCreate,
    OperationRateMaxUpdate,
)
from .ts_yearly_full_load_hour_max import (
    YearlyFullLoadHourMax,
    YearlyFullLoadHourMaxCreate,
    YearlyFullLoadHourMaxUpdate,
)
from .ts_yearly_full_load_hour_min import (
    YearlyFullLoadHourMin,
    YearlyFullLoadHourMinCreate,
    YearlyFullLoadHourMinUpdate,
)
from .user import User, UserCreate, UserInDB, UserUpdate
