from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base import CRUDBase
from ensysmod.model import Generation
from ensysmod.schemas import GenerationCreate, GenerationUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDGeneration(CRUDBase[Generation, GenerationCreate, GenerationUpdate]):
    def create(self, db: Session, *, obj_in: GenerationCreate) -> Generation:
        region_obj = crud.region.get_by_name(obj_in.region)
        if not region_obj:
            raise ValueError(f"Region '{obj_in.region}' does not exist.")

        source_obj = crud.energy_source.get_by_name(obj_in.source)
        if not source_obj:
            raise ValueError(f"Energy source '{obj_in.source}' does not exist.")

        db_obj = Generation(
            year=obj_in.year,
            quantity=obj_in.quantity,
            region=region_obj.id,
            source=source_obj.id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    pass


generation = CRUDGeneration(Generation)
