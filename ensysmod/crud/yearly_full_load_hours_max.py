from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import YearlyFullLoadHoursMax
from ensysmod.schemas import YearlyFullLoadHoursMaxCreate, YearlyFullLoadHoursMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHoursMax(CRUDBaseDependsRegionMatrix[YearlyFullLoadHoursMax, YearlyFullLoadHoursMaxCreate, YearlyFullLoadHoursMaxUpdate]):
    """
    CRUD operations for YearlyFullLoadHoursMax
    """


yearly_full_load_hours_max = CRUDYearlyFullLoadHoursMax(YearlyFullLoadHoursMax, data_column="yearly_full_load_hours_max")
