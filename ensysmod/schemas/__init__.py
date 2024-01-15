"""
This package contains every model that is returned from the Rest-API.
"""
from .dataset import Dataset, DatasetCreate, DatasetUpdate
from .dataset_permission import DatasetPermission, DatasetPermissionCreate, DatasetPermissionUpdate
from .energy_commodity import EnergyCommodity, EnergyCommodityCreate, EnergyCommodityUpdate
from .energy_component import EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate
from .energy_conversion import EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate
from .energy_conversion_factor import EnergyConversionFactor, EnergyConversionFactorCreate, EnergyConversionFactorUpdate
from .energy_model import EnergyModel, EnergyModelCreate, EnergyModelUpdate
from .energy_model_optimization import EnergyModelOptimization, EnergyModelOptimizationCreate, EnergyModelOptimizationUpdate
from .energy_model_override import EnergyModelOverride, EnergyModelOverrideCreate, EnergyModelOverrideUpdate
from .energy_sink import EnergySink, EnergySinkCreate, EnergySinkUpdate
from .energy_source import EnergySource, EnergySourceCreate, EnergySourceUpdate
from .energy_storage import EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate
from .energy_transmission import EnergyTransmission, EnergyTransmissionCreate, EnergyTransmissionUpdate
from .file_upload import FileStatus, FileUploadResult, ZipArchiveUploadResult
from .region import Region, RegionCreate, RegionUpdate
from .token import Token, TokenPayload
from .user import User, UserCreate, UserUpdate

from .capacity_fix import CapacityFix, CapacityFixCreate, CapacityFixUpdate
from .capacity_max import CapacityMax, CapacityMaxCreate, CapacityMaxUpdate
from .capacity_min import CapacityMin, CapacityMinCreate, CapacityMinUpdate
from .operation_rate_fix import OperationRateFix, OperationRateFixCreate, OperationRateFixUpdate
from .operation_rate_max import OperationRateMax, OperationRateMaxCreate, OperationRateMaxUpdate
from .yearly_full_load_hours_max import YearlyFullLoadHoursMax, YearlyFullLoadHoursMaxCreate, YearlyFullLoadHoursMaxUpdate
from .yearly_full_load_hours_min import YearlyFullLoadHoursMin, YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinUpdate
from .transmission_distance import TransmissionDistance, TransmissionDistanceCreate, TransmissionDistanceUpdate
from .transmission_loss import TransmissionLoss, TransmissionLossCreate, TransmissionLossUpdate
