from ensysmod.crud.base_depends_region_x_region_matrix import CRUDBaseDependsRegionXRegionMatrix
from ensysmod.model import TransmissionLoss
from ensysmod.schemas import TransmissionLossCreate, TransmissionLossUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDTransmissionLoss(CRUDBaseDependsRegionXRegionMatrix[TransmissionLoss, TransmissionLossCreate, TransmissionLossUpdate]):
    """
    CRUD operations for TransmissionLoss
    """


transmission_loss = CRUDTransmissionLoss(TransmissionLoss, data_column="loss")
