from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModelOptimization
from ensysmod.schemas import EnergyModelOptimizationCreate, EnergyModelOptimizationUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModelOptimization(CRUDBaseDependsDataset[EnergyModelOptimization, EnergyModelOptimizationCreate, EnergyModelOptimizationUpdate]):
    """
    CRUD operations for EnergyModelOptimization
    """

    def get_by_ref_model(self, db: Session, *, ref_model: int) -> EnergyModelOptimization | None:
        query = select(EnergyModelOptimization).where(EnergyModelOptimization.ref_model == ref_model)
        return db.execute(query).scalar_one_or_none()


energy_model_optimization = CRUDEnergyModelOptimization(EnergyModelOptimization)
