from sqlalchemy.orm import Session

from ensysmod.crud.base import CRUDBase
from ensysmod.model import EnergyTransmissionDistance
from ensysmod.schemas import EnergyTransmissionDistanceCreate, EnergyTransmissionDistanceUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergyTransmissionDistance(CRUDBase[EnergyTransmissionDistance,
                                              EnergyTransmissionDistanceCreate,
                                              EnergyTransmissionDistanceUpdate]):
    """
    CRUD operations for EnergyTransmissionDistance
    """

    def remove_by_component(self, db: Session, component_id: int):
        """
        Removes all EnergyTransmissionDistance entries for a given component.

        :param db: Database session
        :param component_id: ID of the component
        """
        db.query(EnergyTransmissionDistance).filter(EnergyTransmissionDistance.ref_component == component_id).delete()


energy_transmission_distance = CRUDEnergyTransmissionDistance(EnergyTransmissionDistance)
