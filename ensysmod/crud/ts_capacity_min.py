from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import CapacityMin
from ensysmod.schemas import CapacityMinCreate, CapacityMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMin(CRUDBaseDependsTimeSeries[CapacityMin, CapacityMinCreate, CapacityMinUpdate]):
    """
    CRUD operations for CapacityMin
    """
    pass


capacity_min = CRUDCapacityMin(CapacityMin, "min_capacities")
