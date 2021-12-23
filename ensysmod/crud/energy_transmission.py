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

        # also create distances
        if obj_in.distances is not None:
            for distance_create in obj_in.distances:
                distance_create.ref_dataset = obj_in.ref_dataset
                distance_create.ref_component = db_obj.component.id
                crud.energy_transmission_distance.create(db, obj_in=distance_create)

        return db_obj


energy_transmission = CRUDEnergyTransmission(EnergyTransmission)
