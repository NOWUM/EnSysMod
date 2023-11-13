from operator import or_
from typing import Generic

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_component_region import CRUDBaseDependsComponentRegion


class CRUDBaseDependsMatrix(CRUDBaseDependsComponentRegion, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a matrix.
    """

    data_column: str

    def __init__(self, model: type[ModelType], data_column: str):
        super().__init__(model=model)
        self.data_column = data_column

    def get_multi_by_component_and_regions(self, db: Session, *, component_id: int, region_ids: list[int]) -> list[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region.in_(region_ids))
            .filter(or_(self.model.ref_region_to.is_(None), self.model.ref_region_to.in_(region_ids)))
            .all()
        )

    def has_data(self, db: Session, *, component_id: int, region_ids: list[int]) -> bool:
        result = self.get_multi_by_component_and_regions(db=db, component_id=component_id, region_ids=region_ids)
        return result is not None and len(result) > 0

    # TODO reimplement the following methods in CRUD classes that inherit from this class.

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_dict = obj_in.dict()

        # If the data is a list, the length must match the number_of_time_steps of the dataset.
        if isinstance(obj_in_dict[self.data_column], list):
            allowed_len = crud.dataset.get(db, id=obj_in_dict["ref_dataset"]).number_of_time_steps
            if len(obj_in_dict[self.data_column]) != allowed_len:
                raise ValueError(f"Number of elements in {self.data_column} must match number of time steps of the dataset: {allowed_len}.")

        component = crud.energy_component.get_by_dataset_and_name(db, name=obj_in.component, dataset_id=obj_in.ref_dataset)
        # raise exception if not found
        obj_in_dict["ref_component"] = component.id

        region = crud.region.get_by_dataset_and_name(db, name=obj_in.region, dataset_id=obj_in.ref_dataset)
        # raise exception if not found
        obj_in_dict["ref_region"] = region.id

        if obj_in.region_to is not None:
            region_to = crud.region.get_by_dataset_and_name(db, name=obj_in.region_to, dataset_id=obj_in.ref_dataset)
            obj_in_dict["ref_region_to"] = region_to.id

        return super().create(db=db, obj_in=obj_in_dict)

    def get_dataframe(self, db: Session, *, component_id: int, region_ids: list[int]) -> pd.DataFrame:
        """
        Get dataframe for component and multiple regions.
        """
        data = self.get_multi_by_component_and_regions(db=db, component_id=component_id, region_ids=region_ids)

        matrix_mode = any(d.ref_region_to is not None for d in data)

        if matrix_mode and any(d.ref_region_to is None for d in data):
            raise Exception(f"All data for component {component_id} must have a ref_region_to set.")

        if matrix_mode and any(isinstance(getattr(d, self.data_column), list) for d in data):
            raise Exception(f"All data for component {component_id} must have a single value for {self.data_column}.")

        if not matrix_mode and len(data) < len(region_ids):
            missing_regions = set(region_ids) - set([d.ref_region for d in data])
            raise Exception(f"No data found for component {component_id} and region(s) {missing_regions}.")

        if not matrix_mode and len(data) > len(region_ids):
            raise Exception(f"More data found for component {component_id} and region(s) {region_ids}.")

        # Sort data by region
        data = sorted(data, key=lambda d: region_ids.index(d.ref_region))

        if matrix_mode:
            # return two dimensional data frame with regions as columns and indices
            region_names = [crud.region.get(db, id=r_id).name for r_id in region_ids]
            df = pd.DataFrame(0, index=region_names, columns=region_names)
            for d in data:
                df[d.region_to.name][d.region.name] = getattr(d, self.data_column)
            return df

        data_dict = {}
        for c in data:
            value = getattr(c, self.data_column)
            data_dict[c.region.name] = value if isinstance(value, list) else [value]

        return pd.DataFrame(data=data_dict)
