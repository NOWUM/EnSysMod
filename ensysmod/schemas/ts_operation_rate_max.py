from typing import List

from pydantic import BaseModel

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase


class OperationRateMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a max operation rate. Used as a base class for all schemas.
    """
    max_operation_rates: List[float]


class OperationRateMaxCreate(OperationRateMaxBase, RefCRBaseCreate):
    """
    Properties to receive via API on creation of a max operation rate.
    """
    pass


class OperationRateMaxUpdate(OperationRateMaxBase, RefCRBaseUpdate):
    """
    Properties to receive via API on update of a max operation rate.
    """
    pass


class OperationRateMax(OperationRateMaxBase, RefCRBase):
    """
    Properties to return via API for a max operation rate.
    """

    class Config:
        orm_mode = True
