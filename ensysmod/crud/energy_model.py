from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyModel
from ensysmod.schemas import EnergyModelCreate, EnergyModelUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModel(CRUDBase[EnergyModel, EnergyModelCreate, EnergyModelUpdate]):
    """
    CRUD operations for EnergyModel
    """

    def get_multi_by_dataset(
            self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int
    ) -> List[EnergyModel]:
        return db.query(EnergyModel) \
            .filter(EnergyModel.ref_dataset == dataset_id) \
            .offset(skip).limit(limit).all()

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[EnergyModel]:
        return db.query(EnergyModel) \
            .filter(EnergyModel.name == name and EnergyModel.ref_dataset == dataset_id) \
            .first()


energy_model = CRUDEnergyModel(EnergyModel)
