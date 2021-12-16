from typing import Optional, Generic, List

from sqlalchemy.orm import Session

from ensysmod.crud.base import ModelType, CreateSchemaType, UpdateSchemaType
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset


class CRUDBaseDependsTimeSeries(CRUDBaseDependsDataset, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a time series for component and region.
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[ModelType]]:
        return db.query(self.model) \
            .filter(self.model.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) -> Optional[ModelType]:
        return db.query(self.model) \
            .filter(self.model.ref_component == component_id and self.model.ref_region == region_id) \
            .first()
