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
        new_model: EnergyModel = super().create(db, obj_in=obj_in)

        # Also create override and optimiztion parameters and fill in the ref_model
        if obj_in.override_parameters is not None:
            for override_parameter in obj_in.override_parameters:
                override_parameter.ref_model = new_model.id
                crud.energy_model_override.create(db, obj_in=override_parameter)

        if obj_in.optimization_parameters is not None:
            obj_in.optimization_parameters.ref_model = new_model.id
            crud.energy_model_optimization.create(db, obj_in=obj_in.optimization_parameters)

        return new_model


energy_model = CRUDEnergyModel(EnergyModel)
