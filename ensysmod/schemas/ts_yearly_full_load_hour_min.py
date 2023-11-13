from pydantic import BaseModel, Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)


class YearlyFullLoadHourMinBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a YearlyFullLoadHourMin entry. Used as a base class for all schemas.
    """

    min_yearly_full_load_hour: NonNegativeFloat = Field(
        ...,
        description="Min yearly full load hour for a component in a region.",
        example=3000.0,
    )


class YearlyFullLoadHourMinCreate(YearlyFullLoadHourMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHourMin entry.
    """



class YearlyFullLoadHourMinUpdate(YearlyFullLoadHourMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHourMin entry.
    """



class YearlyFullLoadHourMin(YearlyFullLoadHourMinBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHourMin entry.
    """

    class Config:
        orm_mode = True
