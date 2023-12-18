from ensysmod.crud.base_depends_region_x_region_matrix import CRUDBaseDependsRegionXRegionMatrix
from ensysmod.model import TransmissionDistance
from ensysmod.schemas import TransmissionDistanceCreate, TransmissionDistanceUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDTransmissionDistance(CRUDBaseDependsRegionXRegionMatrix[TransmissionDistance, TransmissionDistanceCreate, TransmissionDistanceUpdate]):
    """
    CRUD operations for TransmissionDistance
    """


transmission_distance = CRUDTransmissionDistance(TransmissionDistance, data_column="distance")
