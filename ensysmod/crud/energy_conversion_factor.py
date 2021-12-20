from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyConversionFactor
from ensysmod.schemas import EnergyConversionFactorCreate, EnergyConversionFactorUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyConversionFactor(CRUDBase[EnergyConversionFactor,
                                          EnergyConversionFactorCreate,
                                          EnergyConversionFactorUpdate]):
    """
    CRUD operations for EnergyConversionFactor
    """

    def remove_by_component(self, db: Session, component_id: int):
        """
        Removes all EnergyConversionFactor entries for a given component.

        :param db: Database session
        :param component_id: ID of the component
        """
        db.query(EnergyConversionFactor).filter(EnergyConversionFactor.ref_component == component_id).delete()

    def create(self, db: Session, obj_in: EnergyConversionFactorCreate):
        """
        Creates a new EnergyConversionFactor entry.

        :param db: Database session
        :param obj_in: EnergyConversionFactor entry
        :return: Created EnergyConversionFactor entry
        """
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                                  dataset_id=obj_in.ref_dataset)

        db_obj = EnergyConversionFactor(
            ref_component=obj_in.ref_component,
            ref_commodity=commodity.id,
            conversion_factor=obj_in.conversion_factor
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


energy_conversion_factor = CRUDEnergyConversionFactor(EnergyConversionFactor)
