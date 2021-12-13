from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyModel
from ensysmod.schemas import EnergyModelCreate, EnergyModelUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModel(CRUDBase[EnergyModel, EnergyModelCreate, EnergyModelUpdate]):
    """
    CRUD operations for EnergyModel
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[EnergyModel]:
        return db.query(EnergyModel).filter(EnergyModel.name == name).first()


energy_model = CRUDEnergyModel(EnergyModel)
