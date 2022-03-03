from typing import List

from pydantic import BaseModel, Field
from pydantic.class_validators import validator

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class OperationRateMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a max operation rate. Used as a base class for all schemas.
    """
    max_operation_rates: List[float] = Field(..., description="Max operation rate for a component in a specific "
                                                              "region. Provide single value or a list of values for "
                                                              "each time step in dataset.",
                                             example=[0.95, 0.6, 0.7])

    # validators
    _valid_max_operation_rates = validator("max_operation_rates", allow_reuse=True)(
        validators.validate_max_operation_rates)


class OperationRateMaxCreate(OperationRateMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a max operation rate.
    """
    pass


class OperationRateMaxUpdate(OperationRateMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a max operation rate.
    """
    pass


class OperationRateMax(OperationRateMaxBase, RefCRBase):
    """
    Attributes to return via API for a max operation rate.
    """

    class Config:
        orm_mode = True
