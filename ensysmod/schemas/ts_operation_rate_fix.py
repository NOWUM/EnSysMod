from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class OperationRateFixBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a fix operation rate. Used as a base class for all schemas.
    """

    fix_operation_rates: list[NonNegativeFloat] = Field(
        ...,
        description="Fixed operation rate for a component in a specific region.",
        example=[0.95, 0.6, 0.7],
    )


class OperationRateFixCreate(OperationRateFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a fix operation rate.
    """


class OperationRateFixUpdate(OperationRateFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a fix operation rate.
    """


class OperationRateFix(OperationRateFixBase, RefCRBase):
    """
    Attributes to return via API for a fix operation rate.
    """

    class Config:
        orm_mode = True
