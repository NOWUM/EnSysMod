from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import OperationRateMax
from ensysmod.schemas import OperationRateMaxCreate, OperationRateMaxUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateMax(CRUDBaseDependsExcel[OperationRateMax, OperationRateMaxCreate, OperationRateMaxUpdate]):
    """
    CRUD operations for OperationRateMax
    """


operation_rate_max = CRUDOperationRateMax(OperationRateMax, data_column="operation_rate_max")
