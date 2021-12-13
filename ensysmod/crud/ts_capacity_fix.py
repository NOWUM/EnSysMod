from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import CapacityFix
from ensysmod.schemas import CapacityFixCreate, CapacityFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacityFix(CRUDBase[CapacityFix, CapacityFixCreate, CapacityFixUpdate]):
    """
    CRUD operations for CapacityFix
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[CapacityFix]]:
        return db.query(CapacityFix) \
            .filter(CapacityFix.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) -> Optional[CapacityFix]:
        return db.query(CapacityFix) \
            .filter(CapacityFix.ref_component == component_id and CapacityFix.ref_region == region_id) \
            .first()


capacity_fix = CRUDCapacityFix(CapacityFix)
