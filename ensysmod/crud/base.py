from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod.database.base_class import Base
from ensysmod.schemas.base_schema import CreateSchema, UpdateSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchema)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        return db.execute(query).scalar_one_or_none()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        return db.execute(query).scalars().all()

    def create(self, db: Session, *, obj_in: CreateSchemaType | ModelType | dict[str, Any]) -> ModelType:
        if isinstance(obj_in, self.model):
            db_obj = obj_in
        elif isinstance(obj_in, dict):
            # filter obj_in to only pass fields in model to model's constructor
            data = {k: v for k, v in obj_in.items() if k in self.model.__table__.columns}
            db_obj = self.model(**data)
        else:
            obj_in_data = jsonable_encoder(obj_in, include=set(self.model.__table__.columns.keys()))
            db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        db.delete(obj)
        db.commit()
        return obj
