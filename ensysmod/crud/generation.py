from ensysmod.crud.base import CRUDBase
from ensysmod.model import Generation
from ensysmod.schemas import GenerationCreate, GenerationUpdate
from ensysmod.crud.region import region
from ensysmod.crud.energy_source import energy_source
from sqlalchemy.orm import Session


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDGeneration(CRUDBase[Generation, GenerationCreate, GenerationUpdate]):
    def create(self, db: Session, *, generation: GenerationCreate) -> Generation:
        #DB-getRegion mit Namen xy
        l_region = region.get_by_name(generation.region)
        #DB-getSource mit Namen xy
        l_source = energy_source.get_by_name(generation.source)
        #wenn beide nicht null sind:
        if (not l_region):
            raise ValueError("Region not found!") 
        if (not l_source):
            raise ValueError("Energy-Source not found!") 
        db_obj = Generation(
            year=generation.year,
            quantity=generation.quantity,
            region=l_region,
            source=l_source
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    pass


generation = CRUDGeneration(Generation)
