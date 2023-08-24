from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyTransmission
from ensysmod.schemas import EnergyTransmissionCreate, EnergyTransmissionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyTransmission(CRUDBaseDependsComponent[EnergyTransmission,
                                                      EnergyTransmissionCreate,
                                                      EnergyTransmissionUpdate]):
    """
    CRUD operations for EnergyTransmission
    """

    def create(self, db: Session, *, obj_in: EnergyTransmissionCreate) -> EnergyTransmission:
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                                  dataset_id=obj_in.ref_dataset)
        obj_in_dict = obj_in.dict()
        obj_in_dict['ref_commodity'] = commodity.id
        db_obj = super().create(db=db, obj_in=obj_in_dict)

        return db_obj


energy_transmission = CRUDEnergyTransmission(EnergyTransmission)
