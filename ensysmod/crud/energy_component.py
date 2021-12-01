from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyComponent
from ensysmod.schemas import EnergyComponentCreate, EnergyComponentUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyComponent(CRUDBase[EnergyComponent, EnergyComponentCreate, EnergyComponentUpdate]):
    """
    CRUD operations for EnergyComponent
    """

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[EnergyComponent]:
        return db.query(EnergyComponent) \
            .filter(EnergyComponent.name == name and EnergyComponent.ref_dataset == dataset_id) \
            .first()


energy_component = CRUDEnergyComponent(EnergyComponent)
