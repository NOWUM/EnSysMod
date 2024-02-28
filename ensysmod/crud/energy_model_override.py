from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModelOverride
from ensysmod.schemas import EnergyModelOverrideCreate, EnergyModelOverrideUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyModelOverride(CRUDBaseDependsDataset[EnergyModelOverride, EnergyModelOverrideCreate, EnergyModelOverrideUpdate]):
    """
    CRUD operations for EnergyModelOverride
    """


energy_model_override = CRUDEnergyModelOverride(EnergyModelOverride)
