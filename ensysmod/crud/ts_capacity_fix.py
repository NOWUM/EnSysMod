from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import CapacityFix
from ensysmod.schemas import CapacityFixCreate, CapacityFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityFix(CRUDBaseDependsTimeSeries[CapacityFix, CapacityFixCreate, CapacityFixUpdate]):
    """
    CRUD operations for CapacityFix
    """
    pass


capacity_fix = CRUDCapacityFix(CapacityFix, "fix_capacities")
