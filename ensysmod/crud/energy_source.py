from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.energy_commodity import energy_commodity
from ensysmod.model import EnergySource
from ensysmod.schemas import EnergySourceCreate, EnergySourceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySource(CRUDBaseDependsComponent[EnergySource, EnergySourceCreate, EnergySourceUpdate]):
    """
    CRUD operations for EnergySource
    """

    def create(self, db: Session, *, obj_in: EnergySourceCreate) -> EnergySource:
        commodity = energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                             dataset_id=obj_in.ref_dataset)
        obj_in_dict = obj_in.dict()
        obj_in_dict['ref_commodity'] = commodity.id
        return super().create(db=db, obj_in=obj_in_dict)


energy_source = CRUDEnergySource(EnergySource)
