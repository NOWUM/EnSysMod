from typing import Any, Generic

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyComponent


class CRUDBaseDependsComponent(CRUDBaseDependsDataset, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a component.
    """

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> ModelType | None:
        """
        Get an energy component based object by dataset and name.
        """
        component = crud.energy_component.get_by_dataset_and_name(db, dataset_id=dataset_id, name=name)
        if component is None:
            return None
        query = select(self.model).where(self.model.ref_component == component.id)
        return db.execute(query).scalar_one_or_none()

    def get_multi_by_dataset(self, db: Session, *, skip: int = 0, limit: int = 100, dataset_id: int) -> list[ModelType]:
        """
        Get a list of energy component based objects based on dataset.
        """
        query = select(self.model).join(EnergyComponent).where(EnergyComponent.ref_dataset == dataset_id).offset(skip).limit(limit)
        return db.execute(query).scalars().all()

    def create(self, db: Session, *, obj_in: CreateSchemaType | ModelType | dict[str, Any]) -> ModelType:
        """
        Store an energy component based object in database.
        """
        component = crud.energy_component.create(db, obj_in=obj_in)
        obj_in_dict = jsonable_encoder(obj_in)
        obj_in_dict["ref_component"] = component.id
        return super().create(db, obj_in=obj_in_dict)
