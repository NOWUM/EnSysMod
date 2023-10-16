from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import YearlyFullLoadHourMax
from ensysmod.schemas import YearlyFullLoadHourMaxCreate, YearlyFullLoadHourMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHourMax(CRUDBaseDependsTimeSeries[YearlyFullLoadHourMax, YearlyFullLoadHourMaxCreate, YearlyFullLoadHourMaxUpdate]):
    """
    CRUD operations for YearlyFullLoadHourMax
    """
    pass


yearly_full_load_hour_max = CRUDYearlyFullLoadHourMax(YearlyFullLoadHourMax, "max_yearly_full_load_hour")
