from typing import Generic

from sqlalchemy.orm import Session

from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix


class CRUDBaseDependsRegionXRegionMatrix(CRUDBaseDependsMatrix, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a region x region matrix.
    """

    def get_by_component_and_2_regions(self, db: Session, component_id: int, region_id: int, region_to_id: int) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region == region_id)
            .filter(self.model.ref_region_to == region_to_id)
            .first()
        )

    # TODO implement methods
