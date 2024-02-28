from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModel, EnergyModelOptimization, EnergyModelOverride
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

        # Create override and optimization parameters
        override_parameter_fields = set(EnergyModelOverride.__table__.columns.keys())
        for override_parameter_create in obj_in.override_parameters:
            component = crud.energy_component.get_by_dataset_and_name(
                db, name=override_parameter_create.component_name, dataset_id=new_model.ref_dataset
            )
            if component is None:
                raise ValueError(f"Component {override_parameter_create.component_name} not found in dataset {new_model.ref_dataset}!")

            override_parameter = EnergyModelOverride(
                ref_model=new_model.id,
                ref_component=component.id,
                **override_parameter_create.model_dump(include=override_parameter_fields),
            )
            crud.energy_model_override.create(db, obj_in=override_parameter)

        if obj_in.optimization_parameters is not None:
            optimization_parameter_fields = set(EnergyModelOptimization.__table__.columns.keys())
            optimization_parameters = EnergyModelOptimization(
                ref_model=new_model.id,
                **obj_in.optimization_parameters.model_dump(include=optimization_parameter_fields),
            )
            crud.energy_model_optimization.create(db, obj_in=optimization_parameters)

        return new_model


energy_model = CRUDEnergyModel(EnergyModel)
