from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import CapacityMax
from ensysmod.schemas import CapacityMaxCreate, CapacityMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMax(CRUDBaseDependsRegionMatrix[CapacityMax, CapacityMaxCreate, CapacityMaxUpdate]):
    """
    CRUD operations for CapacityMax
    """


capacity_max = CRUDCapacityMax(CapacityMax, data_column="max_capacity")
