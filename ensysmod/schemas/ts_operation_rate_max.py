from typing import List

from pydantic import BaseModel
from pydantic.class_validators import validator

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class OperationRateMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared properties for a max operation rate. Used as a base class for all schemas.
    """
    max_operation_rates: List[float]

    # validators
    _valid_max_operation_rates = validator("max_operation_rates", allow_reuse=True)(validators.validate_max_operation_rates)


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
