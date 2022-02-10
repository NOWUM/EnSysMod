from typing import Optional, Union, Any

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.crud.dataset_permission import dataset_permission
from ensysmod.model import Dataset
from ensysmod.schemas import DatasetCreate, DatasetUpdate, DatasetPermissionCreate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    """
    CRUD operations for Dataset
    """

    def create(self, db: Session, *, obj_in: Union[DatasetCreate, Dataset, dict]) -> Dataset:
        new_dataset: Dataset = super().create(db, obj_in=obj_in)

        # Add permission for creator
        creator_permission = DatasetPermissionCreate(
            ref_dataset=new_dataset.id,
            ref_user=new_dataset.ref_created_by,
            allow_usage=True,
            allow_modification=True,
            allow_permission_grant=True,
            allow_permission_revoke=True,
        )
        dataset_permission.create(db, obj_in=creator_permission)

        return new_dataset

    def get_by_name(self, db: Session, *, name: str) -> Optional[Dataset]:
        return db.query(Dataset).filter(Dataset.name == name).first()

    def remove(self, db: Session, *, id: Any) -> Dataset:
        dataset_permission.remove_by_dataset(db, dataset_id=id)
        return super().remove(db, id=id)


dataset = CRUDDataset(Dataset)
