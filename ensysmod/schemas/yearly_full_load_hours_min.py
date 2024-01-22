from pydantic import Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class YearlyFullLoadHoursMinBase(RefCRBaseBase):
    """
    Shared attributes for a YearlyFullLoadHoursMin. Used as a base class for all schemas.
    """

    yearly_full_load_hours_min: NonNegativeFloat = Field(
        default=...,
        description="YearlyFullLoadHoursMin for a component in a region.",
        examples=[3000.0],
    )


class YearlyFullLoadHoursMinCreate(YearlyFullLoadHoursMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHoursMin.
    """


class YearlyFullLoadHoursMinUpdate(YearlyFullLoadHoursMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHoursMin.
    """


class YearlyFullLoadHoursMin(YearlyFullLoadHoursMinBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHoursMin.
    """
