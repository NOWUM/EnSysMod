from ensysmod.crud.base_depends_component import CRUDBaseDependsComponent
from ensysmod.model import EnergySink
from ensysmod.schemas import EnergySinkCreate, EnergySinkUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDEnergySink(CRUDBaseDependsComponent[EnergySink, EnergySinkCreate, EnergySinkUpdate]):
    """
    CRUD operations for EnergySink
    """


energy_sink = CRUDEnergySink(EnergySink)
