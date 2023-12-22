from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import CapacityMax
from ensysmod.schemas import CapacityMaxCreate, CapacityMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMax(CRUDBaseDependsExcel[CapacityMax, CapacityMaxCreate, CapacityMaxUpdate]):
    """
    CRUD operations for CapacityMax
    """


capacity_max = CRUDCapacityMax(CapacityMax, data_column="capacity_max")
