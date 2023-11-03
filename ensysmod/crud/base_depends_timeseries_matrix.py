from typing import Generic

from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix


class CRUDBaseDependsTimeSeriesMatrix(CRUDBaseDependsMatrix, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a time series matrix.
    """

    pass
    # TODO implement methods
