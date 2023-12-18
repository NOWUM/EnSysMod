from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import YearlyFullLoadHoursMin
from ensysmod.schemas import YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHoursMin(CRUDBaseDependsRegionMatrix[YearlyFullLoadHoursMin, YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinUpdate]):
    """
    CRUD operations for YearlyFullLoadHoursMin
    """


yearly_full_load_hours_min = CRUDYearlyFullLoadHoursMin(YearlyFullLoadHoursMin, data_column="yearly_full_load_hours_min")
