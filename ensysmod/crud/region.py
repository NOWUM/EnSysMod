from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate, RegionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDRegion(CRUDBaseDependsDataset[Region, RegionCreate, RegionUpdate]):
    pass


region = CRUDRegion(Region)
