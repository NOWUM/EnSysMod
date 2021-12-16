from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyComponent
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyComponent(CRUDBaseDependsDataset[EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate]):
    """
    CRUD operations for EnergyComponent
    """
    pass


energy_component = CRUDEnergyComponent(EnergyComponent)
