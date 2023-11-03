from typing import Generic

from ensysmod.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from ensysmod.crud.base_depends_matrix import CRUDBaseDependsMatrix


class CRUDBaseDependsRegionMatrix(CRUDBaseDependsMatrix, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for all CRUD classes that depend on a region matrix.
    """

    pass
    # TODO implement methods
