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
        if obj_in.parameters is not None:
            for parameter in obj_in.parameters:
                parameter.ref_model = db_obj.id
                parameter.ref_dataset = db_obj.ref_dataset
                crud.energy_model_parameter.create(db, obj_in=parameter)

        return db_obj


energy_model = CRUDEnergyModel(EnergyModel)
