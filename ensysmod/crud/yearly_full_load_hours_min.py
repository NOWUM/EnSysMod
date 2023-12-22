from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import YearlyFullLoadHoursMin
from ensysmod.schemas import YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDYearlyFullLoadHoursMin(CRUDBaseDependsExcel[YearlyFullLoadHoursMin, YearlyFullLoadHoursMinCreate, YearlyFullLoadHoursMinUpdate]):
    """
    CRUD operations for YearlyFullLoadHoursMin
    """


yearly_full_load_hours_min = CRUDYearlyFullLoadHoursMin(YearlyFullLoadHoursMin, data_column="yearly_full_load_hours_min")
