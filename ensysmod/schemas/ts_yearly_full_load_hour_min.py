from pydantic import BaseModel, Field, validator

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)
from ensysmod.utils import validators


class YearlyFullLoadHourMinBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a YearlyFullLoadHourMin entry. Used as a base class for all schemas.
    """

    min_yearly_full_load_hour: list[float] = Field(
        ...,
        description="Min yearly full load hour for a component in a region.",
        example=[1800, 2600, 4500],
    )

    # validators
    _valid_min_yearly_full_load_hour = validator("min_yearly_full_load_hour", allow_reuse=True)(validators.validate_min_yearly_full_load_hour)


class YearlyFullLoadHourMinCreate(YearlyFullLoadHourMinBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHourMin entry.
    """

    pass


class YearlyFullLoadHourMinUpdate(YearlyFullLoadHourMinBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHourMin entry.
    """

    pass


class YearlyFullLoadHourMin(YearlyFullLoadHourMinBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHourMin entry.
    """

    class Config:
        orm_mode = True
