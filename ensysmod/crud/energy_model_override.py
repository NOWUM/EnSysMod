from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModelOverride
from ensysmod.schemas import EnergyModelOverrideCreate, EnergyModelOverrideUpdate

# noinspection PyMethodMayBeStatic,PyArgumentList


class CRUDEnergyModelOverride(CRUDBaseDependsDataset[EnergyModelOverride, EnergyModelOverrideCreate, EnergyModelOverrideUpdate]):
    """
    CRUD operations for EnergyModelOverride
    """

    def create(self, db: Session, *, obj_in: EnergyModelOverrideCreate) -> EnergyModelOverride:
        obj_in_dict = obj_in.model_dump()

        # Fill in the ref_component
        dataset_id = crud.energy_model.get(db, id=obj_in.ref_model).ref_dataset
        component = crud.energy_component.get_by_dataset_and_name(db, name=obj_in.component_name, dataset_id=dataset_id)
        if component is None:
            raise ValueError(f"Component {obj_in.component_name} not found in model {obj_in.ref_model}!")
        obj_in_dict["ref_component"] = component.id

        return super().create(db=db, obj_in=obj_in_dict)


energy_model_override = CRUDEnergyModelOverride(EnergyModelOverride)
