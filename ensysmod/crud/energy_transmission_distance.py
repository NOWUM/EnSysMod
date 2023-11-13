from typing import List, Optional

import pandas as pd
from crud.base_depends_region_x_region_matrix import CRUDBaseDependsRegionXRegionMatrix
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.model import EnergyTransmissionDistance
from ensysmod.schemas import (
    EnergyTransmissionDistanceCreate,
    EnergyTransmissionDistanceUpdate,
)

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyTransmissionDistance(CRUDBaseDependsRegionXRegionMatrix[EnergyTransmissionDistance, EnergyTransmissionDistanceCreate, EnergyTransmissionDistanceUpdate]):
    """
    CRUD operations for EnergyTransmissionDistance
    """

    def get_by_component(self, db: Session, component_id: int) -> Optional[List[EnergyTransmissionDistance]]:
        """
        Get all EnergyTransmissionDistance entries for a given component.
        """
        return db.query(self.model).filter(self.model.ref_component == component_id).all()

    def get_by_component_and_region_ids(
        self, db: Session, component_id: int, region_id: int, region_to_id: int
    ) -> Optional[EnergyTransmissionDistance]:
        """
        Get a EnergyTransmissionDistance entry for a given component id and its two region ids.
        """
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region == region_id)
            .filter(self.model.ref_region_to == region_to_id)
            .first()
        )

    def get_by_dataset_id_component_region_names(
        self, db: Session, dataset_id: int,  component_name: str, region_name: str, region_to_name: str
    ) -> Optional[EnergyTransmissionDistance]:
        """
        Get a EnergyTransmissionDistance entry for a given dataset id, component name and its two region names.
        """
        component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=component_name)
        region = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=region_name)
        region_to = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=region_to_name)
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component.id)
            .filter(self.model.ref_region == region.id)
            .filter(self.model.ref_region_to == region_to.id)
            .first()
        )

    def remove_by_component(self, db: Session, component_id: int) -> Optional[List[EnergyTransmissionDistance]]:
        """
        Removes all EnergyTransmissionDistance entries for a given component.
        """
        obj = db.query(self.model).filter(self.model.ref_component == component_id).all()
        db.query(self.model).filter(self.model.ref_component == component_id).delete()
        db.commit()
        return obj

    def create(self, db: Session, obj_in: EnergyTransmissionDistanceCreate) -> EnergyTransmissionDistance:
        """
        Creates a new energy transmission distance entry between two regions.

        :param db: Database session
        :param obj_in: Input data
        :return: New energy transmission distance entry
        """
        transmission = crud.energy_transmission.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.component)
        if transmission is None or transmission.component.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Component not found or from different dataset.")

        region = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.region)
        if region is None or region.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Origin region not found or from different dataset.")

        region_to = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.region_to)
        if region_to is None or region_to.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Target region not found or from different dataset.")

        db_obj = EnergyTransmissionDistance(
            distance=obj_in.distance,
            ref_component=transmission.ref_component,
            ref_region=region.id,
            ref_region_to=region_to.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_dataframe(self, db: Session, component_id: int, region_ids: List[int]) -> pd.DataFrame:
        """
        Returns the distances for the provided regions as matrix.
        """
        data = (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region.in_(region_ids))
            .filter(self.model.ref_region_to.in_(region_ids))
            .all()
        )

        region_names = [crud.region.get(db, id=r_id).name for r_id in region_ids]
        df = pd.DataFrame(0.0, index=region_names, columns=region_names)
        for d in data:
            df[d.region_to.name][d.region.name] = d.distance
        return df


energy_transmission_distance = CRUDEnergyTransmissionDistance(EnergyTransmissionDistance, data_column="distance")
