from pydantic import Field, NonNegativeFloat

from ensysmod.schemas.base_ref_component_region import RefCRBase, RefCRBaseBase, RefCRBaseCreate, RefCRBaseUpdate


class YearlyFullLoadHoursMaxBase(RefCRBaseBase):
    """
    Shared attributes for a YearlyFullLoadHoursMax. Used as a base class for all schemas.
    """

    yearly_full_load_hours_max: NonNegativeFloat = Field(
        default=...,
        description="Maximum yearly full load hour for a component in a region.",
        examples=[3000.0],
    )


class YearlyFullLoadHoursMaxCreate(YearlyFullLoadHoursMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHoursMax.
    """


class YearlyFullLoadHoursMaxUpdate(YearlyFullLoadHoursMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHoursMax.
    """


class YearlyFullLoadHoursMax(YearlyFullLoadHoursMaxBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHoursMax.
    """
