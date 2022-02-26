from ensysmod.crud.base_depends_timeseries import CRUDBaseDependsTimeSeries
from ensysmod.model import OperationRateFix
from ensysmod.schemas import OperationRateFixCreate, OperationRateFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateFix(CRUDBaseDependsTimeSeries[OperationRateFix, OperationRateFixCreate, OperationRateFixUpdate]):
    """
    CRUD operations for OperationRateFix
    """
    pass


operation_rate_fix = CRUDOperationRateFix(OperationRateFix, "fix_operation_rates")
