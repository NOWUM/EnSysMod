from typing import Optional

from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyConversion
from ensysmod.schemas import EnergyConversionCreate, EnergyConversionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversion(CRUDBase[EnergyConversion, EnergyConversionCreate, EnergyConversionUpdate]):
    """
    CRUD operations for EnergyConversion
    """

    def get_by_dataset_and_name(self, db: Session, *, dataset_id: int, name: str) -> Optional[EnergyConversion]:
        component = crud.energy_component.get_by_dataset_and_name(db, dataset_id=dataset_id, name=name)
        if component is None:
            return None
        return db.query(EnergyConversion).filter(EnergyConversion.ref_component == component.id).first()

    def create(self, db: Session, *, obj_in: EnergyConversionCreate) -> EnergyConversion:
        component = crud.energy_component.create(db, obj_in=obj_in)
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity_unit,
                                                                  dataset_id=obj_in.ref_dataset)

        db_obj = EnergyConversion(
            ref_component=component.id,
            ref_commodity_unit=commodity.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # save energy conversion factors
        for factor_create in obj_in.conversion_factors:
            factor_create.ref_dataset = obj_in.ref_dataset
            factor_create.ref_component = component.id
            print(factor_create)
            crud.energy_conversion_factor.create(db, obj_in=factor_create)

        return db_obj

    def remove(self, db: Session, *, id: int) -> EnergyConversion:
        db_obj = super().remove(db=db, id=id)
        crud.energy_component.remove(db, id=id)
        return db_obj

    # TODO update energy conversion


energy_conversion = CRUDEnergyConversion(EnergyConversion)
