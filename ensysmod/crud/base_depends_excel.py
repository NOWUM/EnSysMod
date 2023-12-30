from typing import Generic

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_component_region import CRUDBaseDependsComponentRegion
from ensysmod.model.region import Region


class CRUDBaseDependsExcel(CRUDBaseDependsComponentRegion, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on an excel file.
    """

    def __init__(self, model: type[ModelType], data_column: str):
        super().__init__(model=model)
        self.data_column = data_column

    def get_by_component_and_2_regions(self, db: Session, component_id: int, region_id: int, region_to_id: int) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region == region_id)
            .filter(self.model.ref_region_to == region_to_id)
            .first()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_dict = obj_in.dict()

        # If the data is a list, the length must match the number_of_time_steps of the dataset.
        if isinstance(obj_in_dict[self.data_column], list):
            allowed_len = crud.dataset.get(db, id=obj_in_dict["ref_dataset"]).number_of_time_steps
            if len(obj_in_dict[self.data_column]) != allowed_len:
                raise ValueError(f"Number of elements in {self.data_column} must match number of time steps of the dataset: {allowed_len}.")

        component = crud.energy_component.get_by_dataset_and_name(db, name=obj_in.component, dataset_id=obj_in.ref_dataset)
        if component is None:
            raise ValueError(f"Component {obj_in.component} not found in dataset {obj_in.ref_dataset}!")
        obj_in_dict["ref_component"] = component.id

        region = crud.region.get_by_dataset_and_name(db, name=obj_in.region, dataset_id=obj_in.ref_dataset)
        if region is None:
            raise ValueError(f"Region {obj_in.region} not found in dataset {obj_in.ref_dataset}!")
        obj_in_dict["ref_region"] = region.id

        if obj_in.region_to is not None:
            region_to = crud.region.get_by_dataset_and_name(db, name=obj_in.region_to, dataset_id=obj_in.ref_dataset)
            if region_to is None:
                raise ValueError(f"Region {obj_in.region_to} not found in dataset {obj_in.ref_dataset}!")
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

            dataframe = pd.DataFrame(0, index=region_names, columns=region_names)
            for d in data:
                dataframe[d.region_to.name][d.region.name] = getattr(d, self.data_column)
            return dataframe

        # otherwise return dataframe with 1 row and regions as columns
        data_dict = {}
        for d in data:
            value = getattr(d, self.data_column)
            data_dict[d.region.name] = value if isinstance(value, list) else [value]
        return pd.DataFrame(data=data_dict)
