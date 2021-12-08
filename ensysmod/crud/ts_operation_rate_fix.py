from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import OperationRateFix
from ensysmod.schemas import OperationRateFixCreate, OperationRateFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateFix(CRUDBase[OperationRateFix, OperationRateFixCreate, OperationRateFixUpdate]):
    """
    CRUD operations for OperationRateFix
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[OperationRateFix]]:
        return db.query(OperationRateFix) \
            .filter(OperationRateFix.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) \
            -> Optional[OperationRateFix]:
        return db.query(OperationRateFix) \
            .filter(OperationRateFix.ref_component == component_id and OperationRateFix.ref_region == region_id) \
            .first()


operation_rate_fix = CRUDOperationRateFix(OperationRateFix)
