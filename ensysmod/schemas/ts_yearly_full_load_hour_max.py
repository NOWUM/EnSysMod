from pydantic import BaseModel, Field, validator

from ensysmod.schemas.base_ref_component_region import (
    RefCRBase,
    RefCRBaseBase,
    RefCRBaseCreate,
    RefCRBaseUpdate,
)
from ensysmod.utils import validators


class YearlyFullLoadHourMaxBase(RefCRBaseBase, BaseModel):
    """
    Shared attributes for a YearlyFullLoadHourMax entry. Used as a base class for all schemas.
    """

    max_yearly_full_load_hour: list[float] = Field(
        ...,
        description="Max yearly full load hour for a component in a region.",
        example=[1800, 2600, 4500],
    )

    # validators
    _valid_max_yearly_full_load_hour = validator("max_yearly_full_load_hour", allow_reuse=True)(validators.validate_max_yearly_full_load_hour)


class YearlyFullLoadHourMaxCreate(YearlyFullLoadHourMaxBase, RefCRBaseCreate):
    """
    Attributes to receive via API on creation of a YearlyFullLoadHourMax entry.
    """

    pass


class YearlyFullLoadHourMaxUpdate(YearlyFullLoadHourMaxBase, RefCRBaseUpdate):
    """
    Attributes to receive via API on update of a YearlyFullLoadHourMax entry.
    """

    pass


class YearlyFullLoadHourMax(YearlyFullLoadHourMaxBase, RefCRBase):
    """
    Attributes to return via API for a YearlyFullLoadHourMax entry.
    """

    class Config:
        orm_mode = True
