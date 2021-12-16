from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergyStorage
from ensysmod.schemas import EnergyStorageCreate, EnergyStorageUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyStorage(CRUDBaseDependsComponent[EnergyStorage, EnergyStorageCreate, EnergyStorageUpdate]):
    """
    CRUD operations for EnergyStorage
    """

    def create(self, db: Session, *, obj_in: EnergyStorageCreate) -> EnergyStorage:
        commodity = crud.energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                                  dataset_id=obj_in.ref_dataset)
        obj_in_dict = obj_in.dict()
        obj_in_dict['ref_commodity'] = commodity.id
        return super().create(db=db, obj_in=obj_in_dict)


energy_storage = CRUDEnergyStorage(EnergyStorage)
