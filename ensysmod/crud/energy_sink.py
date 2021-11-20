from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergySink
from ensysmod.schemas import EnergySinkCreate, EnergySinkUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySink(CRUDBase[EnergySink, EnergySinkCreate, EnergySinkUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[EnergySink]:
        return db.query(EnergySink).filter(EnergySink.name == name).first()


energy_sink = CRUDEnergySink(EnergySink)