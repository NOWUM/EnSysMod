from typing import List, Optional, Generic

from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType


class CRUDBaseDependsDataset(CRUDBase, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a dataset.
    """

    def get_multi_by_dataset(
            self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int
    ) -> List[ModelType]:
        return db.query(self.model) \
            .filter(self.model.ref_dataset == dataset_id) \
            .offset(skip).limit(limit).all()

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[ModelType]:
        return db.query(self.model) \
            .filter(self.model.name == name) \
            .filter(self.model.ref_dataset == dataset_id) \
            .first()
