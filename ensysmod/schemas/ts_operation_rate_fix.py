from typing import List

from pydantic import BaseModel, validator, Field

from ensysmod.schemas.base_ref_component_region import RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate, RefCRBase
from ensysmod.util import validators


class OperationRateFixBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a fix operation rate. Used as a base class for all schemas.
    """
    fix_operation_rates: List[float] = Field(..., description="Fix operation rate for a component in a specific "
                                                              "region. Provide single value or a list of values for "
                                                              "each time step in dataset.",
                                             example=[0.95, 0.6, 0.7])

    # validators
    _valid_fix_operation_rates = validator("fix_operation_rates", allow_reuse=True)(
        validators.validate_fix_operation_rates)


class OperationRateFixCreate(OperationRateFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a fix operation rate.
    """
    pass


class OperationRateFixUpdate(OperationRateFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a fix operation rate.
    """
    pass


class OperationRateFix(OperationRateFixBase, RefCRBase):
    """
    Attributes to return via API for a fix operation rate.
    """

    class Config:
        orm_mode = True
