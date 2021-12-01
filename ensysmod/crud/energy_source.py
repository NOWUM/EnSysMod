from typing import Optional

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergySource
from ensysmod.schemas import EnergySourceCreate, EnergySourceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySource(CRUDBase[EnergySource, EnergySourceCreate, EnergySourceUpdate]):
    """
    CRUD operations for EnergySource
    """

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[EnergySource]:
        component = crud.energy_component.get_by_dataset_and_name(db, dataset_id=dataset_id, name=name)
        if component is None:
            return None
        return db.query(EnergySource).filter(EnergySource.ref_component == component.id).first()

    def create(self, db: Session, *, obj_in: EnergySourceCreate) -> EnergySource:
        component = crud.energy_component.create(db, obj_in=obj_in)
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                                  dataset_id=obj_in.ref_dataset)
        db_obj = EnergySource(
            ref_component=component.id,
            ref_commodity=commodity.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> EnergySource:
        db_obj = super().remove(db=db, id=id)
        crud.energy_component.remove(db, id=id)
        return db_obj

    # TODO update energy source


energy_source = CRUDEnergySource(EnergySource)
