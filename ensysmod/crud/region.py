from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate, RegionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDRegion(CRUDBase[Region, RegionCreate, RegionUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Region]:
        return db.query(Region).filter(Region.name == name).first()


region = CRUDRegion(Region)
