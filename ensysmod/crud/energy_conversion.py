from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversion(CRUDBase[EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate]):
    pass


energy_conversion = CRUDEnergyConversion(EnergyConversion)
