from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import YearlyFullLoadHourMin
from ensysmod.schemas import YearlyFullLoadHourMinCreate, YearlyFullLoadHourMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHourMin(CRUDBaseDependsRegionMatrix[YearlyFullLoadHourMin, YearlyFullLoadHourMinCreate, YearlyFullLoadHourMinUpdate]):
    """
    CRUD operations for YearlyFullLoadHourMin
    """

    pass


yearly_full_load_hour_min = CRUDYearlyFullLoadHourMin(YearlyFullLoadHourMin, data_column="min_yearly_full_load_hour")
