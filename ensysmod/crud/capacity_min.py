from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import CapacityMin
from ensysmod.schemas import CapacityMinCreate, CapacityMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMin(CRUDBaseDependsExcel[CapacityMin, CapacityMinCreate, CapacityMinUpdate]):
    """
    CRUD operations for CapacityMin
    """


capacity_min = CRUDCapacityMin(CapacityMin, data_column="capacity_min")
