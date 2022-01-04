from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import OperationRateMax
from ensysmod.schemas import OperationRateMaxCreate, OperationRateMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateMax(CRUDBaseDependsTimeSeries[OperationRateMax, OperationRateMaxCreate, OperationRateMaxUpdate]):
    """
    CRUD operations for OperationRateMax
    """
    pass


operation_rate_max = CRUDOperationRateMax(OperationRateMax, "max_operation_rates")
