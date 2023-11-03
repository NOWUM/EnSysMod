from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import YearlyFullLoadHourMax
from ensysmod.schemas import YearlyFullLoadHourMaxCreate, YearlyFullLoadHourMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHourMax(CRUDBaseDependsRegionMatrix[YearlyFullLoadHourMax, YearlyFullLoadHourMaxCreate, YearlyFullLoadHourMaxUpdate]):
    """
    CRUD operations for YearlyFullLoadHourMax
    """

    pass


yearly_full_load_hour_max = CRUDYearlyFullLoadHourMax(YearlyFullLoadHourMax, data_column="max_yearly_full_load_hour")
