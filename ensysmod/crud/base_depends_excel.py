from typing import Generic

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import Region


class CRUDBaseDependsExcel(CRUDBaseDependsDataset, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on an excel file.
    """

    def __init__(self, model: type[ModelType], data_column: str) -> None:
        super().__init__(model=model)
        self.data_column = data_column

    def get_multi_by_component(self, db: Session, *, component_id: int) -> list[ModelType]:
        query = select(self.model).where(self.model.ref_component == component_id)
        return db.execute(query).scalars().all()

    def get_by_component_and_region(self, db: Session, *, component_id: int, region_id: int, region_to_id: int | None = None) -> ModelType | None:
        query = select(self.model).where(self.model.ref_component == component_id, self.model.ref_region == region_id)
        if region_to_id is not None:
            query = query.where(self.model.ref_region_to == region_to_id)
        return db.execute(query).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_dict = obj_in.model_dump()

        # If the data is a list, the length must match the number_of_time_steps of the dataset.
        if isinstance(obj_in_dict[self.data_column], list):
            allowed_len = crud.dataset.get(db, id=obj_in_dict["ref_dataset"]).number_of_time_steps
            if len(obj_in_dict[self.data_column]) != allowed_len:
                raise ValueError(f"Number of elements in {self.data_column} must match number of time steps of the dataset: {allowed_len}.")

        component = crud.energy_component.get_by_dataset_and_name(db, name=obj_in.component_name, dataset_id=obj_in.ref_dataset)
        if component is None:
            raise ValueError(f"Component {obj_in.component_name} not found in dataset {obj_in.ref_dataset}!")
        obj_in_dict["ref_component"] = component.id

        region = crud.region.get_by_dataset_and_name(db, name=obj_in.region_name, dataset_id=obj_in.ref_dataset)
        if region is None:
            raise ValueError(f"Region {obj_in.region_name} not found in dataset {obj_in.ref_dataset}!")
        obj_in_dict["ref_region"] = region.id

        if obj_in.region_to_name is not None:
            region_to = crud.region.get_by_dataset_and_name(db, name=obj_in.region_to_name, dataset_id=obj_in.ref_dataset)
            if region_to is None:
                raise ValueError(f"Region {obj_in.region_to_name} not found in dataset {obj_in.ref_dataset}!")
            obj_in_dict["ref_region_to"] = region_to.id

        return super().create(db=db, obj_in=obj_in_dict)

    def get_dataframe(self, db: Session, *, component_id: int) -> pd.DataFrame:
        """
        Get dataframe for component and multiple regions.
        """
        data = self.get_multi_by_component(db=db, component_id=component_id)

        # Sort data by region
        data.sort(key=lambda d: d.ref_region)

        # if region_to is not None, return region x region matrix dataframe
        if any(d.ref_region_to is not None for d in data):
            dataset_id = crud.energy_component.get(db, id=component_id).ref_dataset
            region_names = list(db.execute(select(Region.name).where(Region.ref_dataset == dataset_id)).scalars().all())

            dataframe = pd.DataFrame(0, index=region_names, columns=region_names, dtype=float)
            for d in data:
                dataframe.loc[d.region.name, d.region_to.name] = getattr(d, self.data_column)
            return dataframe

        # otherwise return dataframe with 1 row and regions as columns
        data_dict = {}
        for d in data:
            value = getattr(d, self.data_column)
            data_dict[d.region.name] = value if isinstance(value, list) else [value]
        return pd.DataFrame(data=data_dict)

    def remove_multi_by_component(self, db: Session, *, component_id: int) -> list[ModelType]:
        obj_list = self.get_multi_by_component(db, component_id=component_id)
        for obj in obj_list:
            db.delete(obj)
        db.commit()
        return obj_list
