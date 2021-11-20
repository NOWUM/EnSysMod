from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import Consumption
from ensysmod.schemas import ConsumptionCreate, ConsumptionUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDConsumption(CRUDBase[Consumption, ConsumptionCreate, ConsumptionUpdate]):
    def create(self, db: Session, *, obj_in: ConsumptionCreate) -> Consumption:
        region_obj = crud.region.get_by_name(obj_in.region)
        if not region_obj:
            raise ValueError(f"Region '{obj_in.region}' does not exist.")

        source_obj = crud.energy_source.get_by_name(obj_in.source)
        if not source_obj:
            raise ValueError(f"Energy source '{obj_in.source}' does not exist.")

        sink_obj = crud.energy_sink.get_by_name(obj_in.sink)
        if not sink_obj:
            raise ValueError(f"Energy sink '{obj_in.sink}' does not exist.")

        db_obj = Consumption(
            year=obj_in.year,
            quantity=obj_in.quantity,
            region=region_obj.id,
            source=source_obj.id,
            sink=sink_obj.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


consumption = CRUDConsumption(Consumption)
