from ensysmod.crud.base import CRUDBase
from ensysmod.model import Capacity, capacity
from ensysmod.schemas import CapacityCreate, CapacityUpdate
from ensysmod.crud.region import region
from ensysmod.crud.energy_source import energy_source
from sqlalchemy.orm import Session


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDCapacity(CRUDBase[Capacity, CapacityCreate, CapacityUpdate]):
    def create(self, db: Session, *, capacity: CapacityCreate) -> Capacity:
        #DB-getRegion mit Namen xy
        l_region = region.get_by_name(capacity.region)
        #DB-getSource mit Namen xy
        l_source = energy_source.get_by_name(capacity.source)
        #wenn beide nicht null sind:
        if (not l_region):
            raise ValueError("Region not found!") 
        if (not l_source):
            raise ValueError("Energy-Source not found!") 
        db_obj = Capacity(
            year=capacity.year,
            quantity=capacity.quantity,
            region=l_region,
            source=l_source
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    


capacity = CRUDCapacity(Capacity)
