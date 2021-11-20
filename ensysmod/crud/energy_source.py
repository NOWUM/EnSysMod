from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergySource
from ensysmod.schemas import EnergySourceCreate, EnergySourceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySource(CRUDBase[EnergySource, EnergySourceCreate, EnergySourceUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[EnergySource]:
        return db.query(EnergySource).filter(EnergySource.name == name).first()


energy_source = CRUDEnergySource(EnergySource)
