from typing import List, Optional

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyTransmissionLoss
from ensysmod.schemas import EnergyTransmissionLossCreate, EnergyTransmissionLossUpdate

# TODO this CRUD class should inherit from CRUDBaseDependsRegionXRegionMatrix

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyTransmissionLoss(CRUDBase[EnergyTransmissionLoss, EnergyTransmissionLossCreate, EnergyTransmissionLossUpdate]):
    """
    CRUD operations for EnergyTransmissionLoss
    """

    def get_by_component(self, db: Session, component_id: int) -> Optional[List[EnergyTransmissionLoss]]:
        """
        Get all EnergyTransmissionLoss entries for a given component.
        """
        return db.query(self.model).filter(self.model.ref_component == component_id).all()

    def get_by_component_and_region_ids(
        self, db: Session, component_id: int, region_from_id: int, region_to_id: int
    ) -> Optional[EnergyTransmissionLoss]:
        """
        Get a EnergyTransmissionLoss entry for a given component id and its two region ids.
        """
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region_from == region_from_id)
            .filter(self.model.ref_region_to == region_to_id)
            .first()
        )

    def get_by_dataset_id_component_region_names(
        self, db: Session, dataset_id: int,  component_name: str, region_from_name: str, region_to_name: str
    ) -> Optional[EnergyTransmissionLoss]:
        """
        Get a EnergyTransmissionLoss entry for a given dataset id, component name and its two region names.
        """
        component = crud.energy_component.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=component_name)
        region_from = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=region_from_name)
        region_to = crud.region.get_by_dataset_and_name(db=db, dataset_id=dataset_id, name=region_to_name)
        return (
            db.query(self.model)
            .filter(self.model.ref_component == component.id)
            .filter(self.model.ref_region_from == region_from.id)
            .filter(self.model.ref_region_to == region_to.id)
            .first()
        )

    def remove_by_component(self, db: Session, component_id: int) -> Optional[List[EnergyTransmissionLoss]]:
        """
        Removes all EnergyTransmissionLoss entries for a given component.
        """
        obj = db.query(self.model).filter(self.model.ref_component == component_id).all()
        db.query(self.model).filter(self.model.ref_component == component_id).delete()
        db.commit()
        return obj

    def create(self, db: Session, obj_in: EnergyTransmissionLossCreate) -> EnergyTransmissionLoss:
        """
        Creates a new energy transmission loss entry between two regions.

        :param db: Database session
        :param obj_in: Input data
        :return: New energy transmission loss entry
        """

        transmission = crud.energy_transmission.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.component)
        if transmission is None or transmission.component.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Component not found or from different dataset.")

        region_from = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.region_from)
        if region_from is None or region_from.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Origin region not found or from different dataset.")

        region_to = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.region_to)
        if region_to is None or region_to.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Target region not found or from different dataset.")

        db_obj = EnergyTransmissionLoss(
            loss=obj_in.loss,
            ref_component=transmission.ref_component,
            ref_region_from=region_from.id,
            ref_region_to=region_to.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_dataframe(self, db: Session, component_id: int, region_ids: List[int]) -> pd.DataFrame:
        """
        Returns the losses for the provided regions as matrix.
        """
        data = (
            db.query(self.model)
            .filter(self.model.ref_component == component_id)
            .filter(self.model.ref_region_from.in_(region_ids))
            .filter(self.model.ref_region_to.in_(region_ids))
            .all()
        )

        region_names = [crud.region.get(db, id=r_id).name for r_id in region_ids]
        df = pd.DataFrame(0.0, index=region_names, columns=region_names)
        for d in data:
            df[d.region_to.name][d.region_from.name] = d.loss
        return df


energy_transmission_loss = CRUDEnergyTransmissionLoss(EnergyTransmissionLoss)
