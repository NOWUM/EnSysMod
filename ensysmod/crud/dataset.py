from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import Dataset, DatasetPermission
from ensysmod.schemas import DatasetCreate, DatasetUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    """
    CRUD operations for Dataset
    """

    def create(self, db: Session, *, obj_in: DatasetCreate | Dataset | dict[str, Any]) -> Dataset:
        new_dataset: Dataset = super().create(db, obj_in=obj_in)

        # Create permission for creator
        creator_permission = DatasetPermission(
            ref_dataset=new_dataset.id,
            ref_user=new_dataset.ref_user,
            allow_usage=True,
            allow_modification=True,
            allow_permission_grant=True,
            allow_permission_revoke=True,
        )
        crud.dataset_permission.create(db, obj_in=creator_permission)

        return new_dataset

    def get_by_name(self, db: Session, *, name: str) -> Dataset | None:
        query = select(Dataset).where(Dataset.name == name)
        return db.execute(query).scalar_one_or_none()


dataset = CRUDDataset(Dataset)
