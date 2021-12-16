from typing import Optional, List

from sqlalchemy.orm import Session

from ensysmod.crud.base_depends_dataset import CRUDBaseDependsDataset
from ensysmod.model import EnergyModel
from ensysmod.schemas import EnergyModelCreate, EnergyModelUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyModel(CRUDBaseDependsDataset[EnergyModel, EnergyModelCreate, EnergyModelUpdate]):
    """
    CRUD operations for EnergyModel
    """
    pass


energy_model = CRUDEnergyModel(EnergyModel)
