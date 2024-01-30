from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import DatasetPermission
from ensysmod.schemas import DatasetCreate, DatasetUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDDatasetPermission(CRUDBaseDependsDataset[DatasetPermission, DatasetCreate, DatasetUpdate]):
    """
    CRUD operations for Dataset
    """

    def get_multi_by_user(self, db: Session, *, user_id: int) -> list[DatasetPermission]:
        query = select(self.model).where(self.model.ref_user == user_id)
        return db.execute(query).scalars().all()

    def get_multi_by_dataset(self, db: Session, *, dataset_id: int) -> list[DatasetPermission]:
        query = select(self.model).where(self.model.ref_dataset == dataset_id)
        return db.execute(query).scalars().all()

    def get_by_dataset_and_user(self, db: Session, *, dataset_id: int, user_id: int) -> DatasetPermission | None:
        query = select(self.model).where(self.model.ref_dataset == dataset_id, self.model.ref_user == user_id)
        return db.execute(query).scalar_one_or_none()

    def is_usage_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = self.get_by_dataset_and_user(db=db, dataset_id=dataset_id, user_id=user_id)
        if permission is None:
            return False
        return permission.allow_usage

    def is_modification_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = self.get_by_dataset_and_user(db=db, dataset_id=dataset_id, user_id=user_id)
        if permission is None:
            return False
        return permission.allow_modification

    def is_permission_grant_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = self.get_by_dataset_and_user(db=db, dataset_id=dataset_id, user_id=user_id)
        if permission is None:
            return False
        return permission.allow_permission_grant

    def is_permission_revoke_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = self.get_by_dataset_and_user(db=db, dataset_id=dataset_id, user_id=user_id)
        if permission is None:
            return False
        return permission.allow_permission_revoke

    def is_permission_check_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = self.get_by_dataset_and_user(db=db, dataset_id=dataset_id, user_id=user_id)
        return permission is not None


dataset_permission = CRUDDatasetPermission(DatasetPermission)
