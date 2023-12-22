from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import TransmissionDistance
from ensysmod.schemas import TransmissionDistanceCreate, TransmissionDistanceUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDTransmissionDistance(CRUDBaseDependsExcel[TransmissionDistance, TransmissionDistanceCreate, TransmissionDistanceUpdate]):
    """
    CRUD operations for TransmissionDistance
    """


transmission_distance = CRUDTransmissionDistance(TransmissionDistance, data_column="distance")
