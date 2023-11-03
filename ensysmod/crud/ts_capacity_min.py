from ensysmod.crud.base_depends_region_matrix import CRUDBaseDependsRegionMatrix
from ensysmod.model import CapacityMin
from ensysmod.schemas import CapacityMinCreate, CapacityMinUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMin(CRUDBaseDependsRegionMatrix[CapacityMin, CapacityMinCreate, CapacityMinUpdate]):
    """
    CRUD operations for CapacityMin
    """

    pass


capacity_min = CRUDCapacityMin(CapacityMin, data_column="min_capacities")
