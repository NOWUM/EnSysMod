from typing import List

from pydantic import BaseModel

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase


class OperationRateFixBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a fix operation rate. Used as a base class for all schemas.
    """
    fix_operation_rates: List[float]


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
