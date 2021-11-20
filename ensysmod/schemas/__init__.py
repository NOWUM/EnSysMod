"""
This package contains every model that is returned from the Rest-API.
"""
from .capacity import Capacity, CapacityCreate, CapacityUpdate, CapacityInDB
from .consumption import Consumption, ConsumptionCreate, ConsumptionUpdate, ConsumptionInDB
from .energy_conversion import EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate, EnergyConversionInDB
from .energy_sink import EnergySink, EnergySinkCreate, EnergySinkUpdate, EnergySinkInDB
from .energy_source import EnergySource, EnergySourceCreate, EnergySourceUpdate, EnergySourceInDB
from .energy_storage import EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate, EnergyStorageInDB
from .generation import Generation, GenerationCreate, GenerationUpdate, GenerationInDB
from .region import Region, RegionCreate, RegionUpdate, RegionInDB
from .token import Token, TokenPayload
from .user import User, UserCreate, UserInDB, UserUpdate
