from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import YearlyFullLoadHourMin
from ensysmod.schemas import YearlyFullLoadHourMinCreate, YearlyFullLoadHourMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHourMin(CRUDBaseDependsTimeSeries[YearlyFullLoadHourMin, YearlyFullLoadHourMinCreate, YearlyFullLoadHourMinUpdate]):
    """
    CRUD operations for YearlyFullLoadHourMin
    """
    pass


yearly_full_load_hour_min = CRUDYearlyFullLoadHourMin(YearlyFullLoadHourMin, "min_yearly_full_load_hour")
