from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class OperationRateMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a max operation rate. Used as a base class for all schemas.
    """

    max_operation_rates: list[NonNegativeFloat] = Field(
        ...,
        description="Maximum operation rate for a component in a specific region.",
        example=[0.95, 0.6, 0.7],
    )


class OperationRateMaxCreate(OperationRateMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a max operation rate.
    """


class OperationRateMaxUpdate(OperationRateMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a max operation rate.
    """


class OperationRateMax(OperationRateMaxBase, RefCRBase):
    """
    Attributes to return via API for a max operation rate.
    """

    class Config:
        orm_mode = True
