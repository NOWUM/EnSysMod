from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import CapacityFix
from ensysmod.schemas import CapacityFixCreate, CapacityFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityFix(CRUDBaseDependsRegionMatrix[CapacityFix, CapacityFixCreate, CapacityFixUpdate]):
    """
    CRUD operations for CapacityFix
    """


capacity_fix = CRUDCapacityFix(CapacityFix, data_column="capacity_fix")
