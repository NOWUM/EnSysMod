from ensysmod.crud.base_depends_excel import CRUDBaseDependsExcel
from ensysmod.model import OperationRateFix
from ensysmod.schemas import OperationRateFixCreate, OperationRateFixUpdate


# noinspection PyMethodMayBeStatic,PyArgumentList
class CRUDOperationRateFix(CRUDBaseDependsExcel[OperationRateFix, OperationRateFixCreate, OperationRateFixUpdate]):
    """
    CRUD operations for OperationRateFix
    """


operation_rate_fix = CRUDOperationRateFix(OperationRateFix, data_column="operation_rate_fix")
