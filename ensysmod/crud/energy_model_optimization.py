from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModelOptimization
from ensysmod.schemas import (
    EnergyModelOptimizationCreate,
    EnergyModelOptimizationUpdate,
)


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModelOptimization(CRUDBaseDependsDataset[EnergyModelOptimization, EnergyModelOptimizationCreate, EnergyModelOptimizationUpdate]):
    """
    CRUD operations for EnergyModelOptimization
    """

    def create(self, db: Session, *, obj_in: EnergyModelOptimizationCreate) -> EnergyModelOptimization:
        db_obj: EnergyModelOptimization = super().create(db, obj_in=obj_in)

        return db_obj

    def get_by_ref_model(self, db: Session, *, ref_model: int) -> Optional[EnergyModelOptimization]:
        return db.query(EnergyModelOptimization).filter(EnergyModelOptimization.ref_model == ref_model).first()


energy_model_optimization = CRUDEnergyModelOptimization(EnergyModelOptimization)
