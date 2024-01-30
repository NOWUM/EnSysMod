from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyStorage
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyStorage(CRUDBaseDependsComponent[EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate]):
    """
    CRUD operations for EnergyStorage
    """


energy_storage = CRUDEnergyStorage(EnergyStorage)
