from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class YearlyFullLoadHourMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a YearlyFullLoadHourMax entry. Used as a base class for all schemas.
    """

    max_yearly_full_load_hour: NonNegativeFloat = Field(
        ...,
        description="Maximum yearly full load hour for a component in a region.",
        example=3000.0,
    )


class YearlyFullLoadHourMaxCreate(YearlyFullLoadHourMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHourMax entry.
    """


class YearlyFullLoadHourMaxUpdate(YearlyFullLoadHourMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHourMax entry.
    """


class YearlyFullLoadHourMax(YearlyFullLoadHourMaxBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHourMax entry.
    """

    class Config:
        orm_mode = True
