from ensysmod.crud.base_depends_timeseries_matrix import CRUDBaseDependsTimeSeriesMatrix
from ensysmod.model import OperationRateFix
from ensysmod.schemas import OperationRateFixCreate, OperationRateFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateFix(CRUDBaseDependsTimeSeriesMatrix[OperationRateFix, OperationRateFixCreate, OperationRateFixUpdate]):
    """
    CRUD operations for OperationRateFix
    """

    pass


operation_rate_fix = CRUDOperationRateFix(OperationRateFix, data_column="fix_operation_rates")
