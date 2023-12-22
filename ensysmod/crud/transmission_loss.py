from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import TransmissionLoss
from ensysmod.schemas import TransmissionLossCreate, TransmissionLossUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDTransmissionLoss(CRUDBaseDependsExcel[TransmissionLoss, TransmissionLossCreate, TransmissionLossUpdate]):
    """
    CRUD operations for TransmissionLoss
    """


transmission_loss = CRUDTransmissionLoss(TransmissionLoss, data_column="loss")
