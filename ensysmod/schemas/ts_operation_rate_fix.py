from typing import List

from pydantic import BaseModel, validator

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class OperationRateFixBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a fix operation rate. Used as a base class for all schemas.
    """
    fix_operation_rates: List[float]

    # validators
    _valid_fix_operation_rates = validator("fix_operation_rates", allow_reuse=True)(validators.validate_fix_operation_rates)


class OperationRateFixCreate(OperationRateFixBase, RefCRBaseCreate):
    """
    Properties to receive via API on creation of a fix operation rate.
    """
    pass


class OperationRateFixUpdate(OperationRateFixBase, RefCRBaseUpdate):
    """
    Properties to receive via API on update of a fix operation rate.
    """
    pass


class OperationRateFix(OperationRateFixBase, RefCRBase):
    """
    Properties to return via API for a fix operation rate.
    """

    class Config:
        orm_mode = True
