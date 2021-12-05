from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import Region
from ensysmod.schemas import RegionCreate, RegionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDRegion(CRUDBase[Region, RegionCreate, RegionUpdate]):
    def get_multi_by_dataset(
            self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int
    ) -> List[Region]:
        return db.query(Region) \
            .filter(Region.ref_dataset == dataset_id) \
            .offset(skip).limit(limit).all()

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[Region]:
        return db.query(Region).filter(Region.name == name and Region.ref_dataset == dataset_id).first()


region = CRUDRegion(Region)
