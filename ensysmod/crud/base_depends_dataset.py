from typing import Generic

from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod.crud.base import CreateSchemaType, CRUDBase, ModelType, UpdateSchemaType


class CRUDBaseDependsDataset(CRUDBase, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a dataset.
    """

    def get_multi_by_dataset(self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int) -> list[ModelType]:
        query = select(self.model).where(self.model.ref_dataset == dataset_id).order_by(self.model.id).offset(skip).limit(limit)
        return db.execute(query).scalars().all()

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> ModelType | None:
        query = select(self.model).where(self.model.ref_dataset == dataset_id, self.model.name == name)
        return db.execute(query).scalar_one_or_none()
