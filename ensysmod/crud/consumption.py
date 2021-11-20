from ensysmod.crud.base import CRUDBase
from ensysmod.model import Consumption
from ensysmod.schemas import ConsumptionCreate, ConsumptionUpdate
from ensysmod.crud.region import region
from ensysmod.crud.energy_source import energy_source
from ensysmod.crud.energy_sink import energy_sink
from sqlalchemy.orm import Session


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDConsumption(CRUDBase[Consumption, ConsumptionCreate, ConsumptionUpdate]):
    def create(self, db: Session, *, consumption: ConsumptionCreate) -> Consumption:
        #DB-getRegion mit Namen xy
        l_region = region.get_by_name(consumption.region)
        #DB-getSource mit Namen xy
        l_source = energy_source.get_by_name(consumption.source)
        #DB-getSink mit Namen xy
        l_sink = energy_sink.get_by_name(consumption.sink)
        #wenn beide nicht null sind:
        if (not l_region):
            raise ValueError("Region not found!") 
        if (not l_source):
            raise ValueError("Energy-Source not found!") 
        if (not l_sink):
            raise ValueError("Energy-Sink not found!") 
        db_obj = Consumption(
            year=consumption.year,
            quantity=consumption.quantity,
            region=l_region,
            source=l_source,
            sink=l_sink
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


consumption = CRUDConsumption(Consumption)
