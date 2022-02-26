from typing import Optional, Generic, List, Union, Dict

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import ModelType, CreateSchemaType, UpdateSchemaType
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset


class CRUDBaseDependsComponentRegion(CRUDBaseDependsDataset, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a component and region.
    """

    def get_by_component(self, db: Session, *, component_id: int) -> Optional[List[ModelType]]:
        return db.query(self.model) \
            .filter(self.model.ref_component == component_id) \
            .all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int) -> Optional[ModelType]:
        return db.query(self.model) \
            .filter(self.model.ref_component == component_id) \
            .filter(self.model.ref_region == region_id) \
            .first()

    def create(self, db: Session, *, obj_in: Union[CreateSchemaType, Dict]) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_dict = obj_in
        else:
            obj_in_dict = obj_in.dict()

        if 'ref_component' not in obj_in_dict:
            component = crud.energy_component.get_by_dataset_and_name(db, name=obj_in_dict['component'],
                                                                      dataset_id=obj_in_dict['ref_dataset'])
            obj_in_dict['ref_component'] = component.id

        if 'region' in obj_in_dict and obj_in_dict['region'] is not None:
            region = crud.region.get_by_dataset_and_name(db, name=obj_in_dict['region'],
                                                         dataset_id=obj_in_dict['ref_dataset'])
            obj_in_dict['ref_region'] = region.id

        if 'region_to' in obj_in_dict and obj_in_dict['region_to'] is not None:
            region_to = crud.region.get_by_dataset_and_name(db, name=obj_in_dict['region_to'],
                                                            dataset_id=obj_in_dict['ref_dataset'])
            obj_in_dict['ref_region_to'] = region_to.id

        return super().create(db=db, obj_in=obj_in_dict)
