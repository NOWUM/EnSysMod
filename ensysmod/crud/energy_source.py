from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergySource
from ensysmod.schemas import EnergySourceCreate, EnergySourceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySource(CRUDBaseDependsComponent[EnergySource, EnergySourceCreate, EnergySourceUpdate]):
    """
    CRUD operations for EnergySource
    """


energy_source = CRUDEnergySource(EnergySource)
