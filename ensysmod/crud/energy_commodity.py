from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyCommodity
from ensysmod.schemas import EnergyCommodityCreate, EnergyCommodityUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyCommodity(CRUDBase[EnergyCommodity, EnergyCommodityCreate, EnergyCommodityUpdate]):
    """
    CRUD operations for EnergyCommodity
    """

    def get_multi_by_dataset(
            self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int
    ) -> List[EnergyCommodity]:
        return db.query(EnergyCommodity) \
            .filter(EnergyCommodity.ref_dataset == dataset_id) \
            .offset(skip).limit(limit).all()

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[EnergyCommodity]:
        return db.query(EnergyCommodity) \
            .filter(EnergyCommodity.name == name and EnergyCommodity.ref_dataset == dataset_id) \
            .first()


energy_commodity = CRUDEnergyCommodity(EnergyCommodity)
