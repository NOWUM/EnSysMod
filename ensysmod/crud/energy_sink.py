from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.crud.energy_commodity import energy_commodity
from ensysmod.model import EnergySink
from ensysmod.schemas import EnergySinkCreate, EnergySinkUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySink(CRUDBaseDependsComponent[EnergySink, EnergySinkCreate, EnergySinkUpdate]):
    """
    CRUD operations for EnergySink
    """

    def create(self, db: Session, *, obj_in: EnergySinkCreate) -> EnergySink:
        commodity = energy_commodity.get_by_dataset_and_name(db, name=obj_in.commodity,
                                                             dataset_id=obj_in.ref_dataset)
        obj_in_dict = obj_in.dict()
        obj_in_dict['ref_commodity'] = commodity.id
        return super().create(db=db, obj_in=obj_in_dict)


energy_sink = CRUDEnergySink(EnergySink)
