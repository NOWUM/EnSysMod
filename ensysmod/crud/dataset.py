from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate, DatasetUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    """
    CRUD operations for Dataset
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[Dataset]:
        return db.query(Dataset).filter(Dataset.name == name).first()


dataset = CRUDDataset(Dataset)
