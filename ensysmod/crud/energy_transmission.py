from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyTransmission
from ensysmod.schemas import EnergyTransmissionCreate, EnergyTransmissionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyTransmission(CRUDBaseDependsComponent[EnergyTransmission, EnergyTransmissionCreate, EnergyTransmissionUpdate]):
    """
    CRUD operations for EnergyTransmission
    """


energy_transmission = CRUDEnergyTransmission(EnergyTransmission)
