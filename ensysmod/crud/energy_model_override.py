from ensysmod.crud.base_depends_component_region import CRUDBaseDependsComponentRegion
from ensysmod.model import EnergyModelOverride
from ensysmod.schemas import EnergyModelOverrideCreate, EnergyModelOverrideUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyModelOverride(CRUDBaseDependsComponentRegion[EnergyModelOverride, EnergyModelOverrideCreate,
                                                             EnergyModelOverrideUpdate]):
    """
    CRUD operations for EnergyModelOverride
    """
    pass


energy_model_override = CRUDEnergyModelOverride(EnergyModelOverride)
