from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import OperationRateMax
from ensysmod.schemas import OperationRateMaxCreate, OperationRateMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateMax(CRUDBase[OperationRateMax, OperationRateMaxCreate, OperationRateMaxUpdate]):
    """
    CRUD operations for OperationRateMax
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[OperationRateMax]]:
        return db.query(OperationRateMax) \
            .filter(OperationRateMax.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) \
            -> Optional[OperationRateMax]:
        return db.query(OperationRateMax) \
            .filter(OperationRateMax.ref_component == component_id and OperationRateMax.ref_region == region_id) \
            .first()


operation_rate_max = CRUDOperationRateMax(OperationRateMax)
