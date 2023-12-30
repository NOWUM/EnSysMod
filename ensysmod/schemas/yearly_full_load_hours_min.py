from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class YearlyFullLoadHoursMinBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a YearlyFullLoadHoursMin entry. Used as a base class for all schemas.
    """

    yearly_full_load_hours_min: NonNegativeFloat = Field(
        ...,
        description="YearlyFullLoadHoursMin for a component in a region.",
        example=3000.0,
    )


class YearlyFullLoadHoursMinCreate(YearlyFullLoadHoursMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHoursMin entry.
    """


class YearlyFullLoadHoursMinUpdate(YearlyFullLoadHoursMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHoursMin entry.
    """


class YearlyFullLoadHoursMin(YearlyFullLoadHoursMinBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHoursMin entry.
    """

    class Config:
        orm_mode = True
