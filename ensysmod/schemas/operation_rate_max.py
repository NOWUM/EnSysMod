from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class OperationRateMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a OperationRateMax. Used as a base class for all schemas.
    """

    operation_rate_max: list[NonNegativeFloat] = Field(
        ...,
        description="Maximum operation rate for a component in a specific region.",
        example=[0.95, 0.6, 0.7],
    )


class OperationRateMaxCreate(OperationRateMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a OperationRateMax.
    """


class OperationRateMaxUpdate(OperationRateMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a OperationRateMax.
    """


class OperationRateMax(OperationRateMaxBase, RefCRBase):
    """
    Attributes to return via API for a OperationRateMax.
    """

    class Config:
        orm_mode = True
