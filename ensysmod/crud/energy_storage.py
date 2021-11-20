from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyStorage
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyStorage(CRUDBase[EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate]):
    pass


energy_storage = CRUDEnergyStorage(EnergyStorage)
