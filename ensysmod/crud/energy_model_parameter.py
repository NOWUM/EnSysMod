from ensysmod.crud.base_depends_component_region import CRUDBaseDependsComponentRegion
from ensysmod.model import EnergyModelParameter
from ensysmod.schemas import EnergyModelParameterCreate, EnergyModelParameterUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyModelParameter(CRUDBaseDependsComponentRegion[EnergyModelParameter, EnergyModelParameterCreate,
                                                              EnergyModelParameterUpdate]):
    """
    CRUD operations for EnergyModelParameter
    """
    pass


energy_model_parameter = CRUDEnergyModelParameter(EnergyModelParameter)
