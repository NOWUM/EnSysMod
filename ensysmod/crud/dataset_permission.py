from typing import Optional

from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import DatasetPermission
from ensysmod.schemas import DatasetCreate, DatasetUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDDatasetPermission(CRUDBaseDependsDataset[DatasetPermission, DatasetCreate, DatasetUpdate]):
    """
    CRUD operations for Dataset
    """

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[DatasetPermission]:
        raise NotImplementedError

    def remove_by_dataset(self, db: Session, *, dataset_id: int) -> None:
        db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id).delete()

    def is_usage_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id,
                                                 DatasetPermission.ref_user == user_id).one_or_none()
        if permission is None:
            return False
        return permission.allow_usage

    def is_modification_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id,
                                                 DatasetPermission.ref_user == user_id).one_or_none()
        if permission is None:
            return False
        return permission.allow_modification

    def is_permission_grant_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id,
                                                 DatasetPermission.ref_user == user_id).one_or_none()
        if permission is None:
            return False
        return permission.allow_permission_grant

    def is_permission_revoke_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id,
                                                 DatasetPermission.ref_user == user_id).one_or_none()
        if permission is None:
            return False
        return permission.allow_permission_revoke

    def is_permission_check_allowed(self, db: Session, *, dataset_id: int, user_id: int) -> bool:
        permission = db.query(self.model).filter(DatasetPermission.ref_dataset == dataset_id,
                                                 DatasetPermission.ref_user == user_id).one_or_none()
        if permission is None:
            return False
        return permission.allow_permission_grant or permission.allow_permission_revoke


dataset_permission = CRUDDatasetPermission(DatasetPermission)
