from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import CapacityMax
from ensysmod.schemas import CapacityMaxCreate, CapacityMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMax(CRUDBaseDependsTimeSeries[CapacityMax, CapacityMaxCreate, CapacityMaxUpdate]):
    """
    CRUD operations for CapacityMax
    """
    pass


capacity_max = CRUDCapacityMax(CapacityMax, "max_capacities")
