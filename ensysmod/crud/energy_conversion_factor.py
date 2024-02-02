from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyConversionFactor
from ensysmod.schemas import EnergyConversionFactorCreate, EnergyConversionFactorUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversionFactor(CRUDBase[EnergyConversionFactor, EnergyConversionFactorCreate, EnergyConversionFactorUpdate]):
    """
    CRUD operations for EnergyConversionFactor
    """


energy_conversion_factor = CRUDEnergyConversionFactor(EnergyConversionFactor)
