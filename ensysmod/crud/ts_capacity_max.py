from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import CapacityMax
from ensysmod.schemas import CapacityMaxCreate, CapacityMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityMax(CRUDBase[CapacityMax, CapacityMaxCreate, CapacityMaxUpdate]):
    """
    CRUD operations for CapacityMax
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[CapacityMax]]:
        return db.query(CapacityMax) \
            .filter(CapacityMax.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) -> Optional[CapacityMax]:
        return db.query(CapacityMax) \
            .filter(CapacityMax.ref_component == component_id and CapacityMax.ref_region == region_id) \
            .first()


capacity_max = CRUDCapacityMax(CapacityMax)
