from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyTransmissionDistance
from ensysmod.schemas import EnergyTransmissionDistanceCreate, EnergyTransmissionDistanceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyTransmissionDistance(CRUDBase[EnergyTransmissionDistance,
                                              EnergyTransmissionDistanceCreate,
                                              EnergyTransmissionDistanceUpdate]):
    """
    CRUD operations for EnergyTransmissionDistance
    """

    def remove_by_component(self, db: Session, component_id: int):
        """
        Removes all EnergyTransmissionDistance entries for a given component.

        :param db: Database session
        :param component_id: ID of the component
        """
        db.query(EnergyTransmissionDistance).filter(EnergyTransmissionDistance.ref_component == component_id).delete()

    def create(self, db: Session, obj_in: EnergyTransmissionDistanceCreate) -> EnergyTransmissionDistance:
        """
        Creates a new energy transmission distance entry between two regions.

        :param db: Database session
        :param obj_in: Input data
        :return: New energy transmission distance entry
        """

        if obj_in.ref_component is None and obj_in.component is None:
            raise ValueError("Component must be specified. Provide reference id or component name.")

        if obj_in.ref_region_from is None and obj_in.region_from is None:
            raise ValueError("Region from must be specified. Provide reference id or region name.")

        if obj_in.ref_component is not None:
            transmission = crud.energy_transmission.get(db, obj_in.ref_component)
        else:
            transmission = crud.energy_transmission.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset,
                                                                            name=obj_in.component)

        if transmission is None or transmission.component.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Component not found or from different dataset.")
        obj_in.ref_component = transmission.ref_component

        if obj_in.ref_region_from is not None:
            region_from = crud.region.get(db, obj_in.ref_region_from)
        else:
            region_from = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset,
                                                              name=obj_in.region_from)

        if region_from is None or region_from.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Region from not found or from different dataset.")
        obj_in.ref_region_from = region_from.id

        if obj_in.ref_region_to is not None:
            region_to = crud.region.get(db, obj_in.ref_region_to)
        else:
            region_to = crud.region.get_by_dataset_and_name(db, dataset_id=obj_in.ref_dataset, name=obj_in.region_to)

        if region_to is None or region_to.ref_dataset != obj_in.ref_dataset:
            raise ValueError("Region to not found or from different dataset.")
        obj_in.ref_region_to = region_to.id

        return super().create(db=db, obj_in=obj_in)

    def get_dataframe(self, db: Session, component_id: int, region_ids: List[int]) -> pd.DataFrame:
        """
        Returns the distances for the provided regions as matrix.
        """
        data = db.query(self.model) \
            .filter(self.model.ref_component == component_id) \
            .filter(self.model.ref_region_from.in_(region_ids)) \
            .filter(self.model.ref_region_to.in_(region_ids)) \
            .all()

        region_names = [crud.region.get(db, id=r_id).name for r_id in region_ids]
        df = pd.DataFrame(0.0, index=region_names, columns=region_names)
        for d in data:
            df[d.region_to.name][d.region_from.name] = d.distance
        return df


energy_transmission_distance = CRUDEnergyTransmissionDistance(EnergyTransmissionDistance)
