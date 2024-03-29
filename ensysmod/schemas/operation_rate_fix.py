from pydantic import Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class OperationRateFixBase(RefCRBaseBase):
    """
    Shared attributes for a OperationRateFix. Used as a base class for all schemas.
    """

    operation_rate_fix: list[NonNegativeFloat] = Field(
        default=...,
        description="Fixed operation rate for a component in a specific region.",
        examples=[[0.95, 0.6, 0.7]],
    )


class OperationRateFixCreate(OperationRateFixBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a OperationRateFix.
    """


class OperationRateFixUpdate(OperationRateFixBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a OperationRateFix.
    """


class OperationRateFixSchema(OperationRateFixBase, RefCRBase):
    """
    Attributes to return via API for a OperationRateFix.
    """
