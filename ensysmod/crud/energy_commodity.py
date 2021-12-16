from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyCommodity

from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyCommodity(CRUDBaseDependsDataset[EnergyCommodity, EnergyCommodityCreate, EnergyCommodityUpdate]):
    """
    CRUD operations for EnergyCommodity
    """
    pass


energy_commodity = CRUDEnergyCommodity(EnergyCommodity)
