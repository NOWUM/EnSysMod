from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModel
from ensysmod.schemas import EnergyModelCreate, EnergyModelUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModel(CRUDBaseDependsDataset[EnergyModel, EnergyModelCreate, EnergyModelUpdate]):
    """
    CRUD operations for EnergyModel
    """

    def create(self, db: Session, *, obj_in: EnergyModelCreate) -> EnergyModel:
        """
        Create a new energy model
        """
        db_obj: EnergyModel = super().create(db, obj_in=obj_in)

        # also create parameters
        if obj_in.override_parameters is not None:
            for parameter in obj_in.override_parameters:
                parameter.ref_model = db_obj.id
                parameter.ref_dataset = db_obj.ref_dataset
                crud.energy_model_override.create(db, obj_in=parameter)

        if obj_in.optimization_parameters is not None:
            obj_in.optimization_parameters.ref_model = db_obj.id
            crud.energy_model_optimization.create(db, obj_in=obj_in.optimization_parameters)

        return db_obj


energy_model = CRUDEnergyModel(EnergyModel)
