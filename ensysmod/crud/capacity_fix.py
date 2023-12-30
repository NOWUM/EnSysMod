from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import CapacityFix
from ensysmod.schemas import CapacityFixCreate, CapacityFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityFix(CRUDBaseDependsExcel[CapacityFix, CapacityFixCreate, CapacityFixUpdate]):
    """
    CRUD operations for CapacityFix
    """


capacity_fix = CRUDCapacityFix(CapacityFix, data_column="capacity_fix")
