from pydantic import Field

from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import DatasetSchema


class RegionBase(BaseSchema):
    """
    Shared attributes for a region. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="Unique name of the region.",
        examples=["germany"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class RegionCreate(RegionBase, CreateSchema):
    """
    Attributes to receive via API on creation of a region.
    """

    ref_dataset: int = Field(
        default=...,
        description="ID of the dataset to use as reference.",
        examples=[1],
        gt=0,
    )


class RegionUpdate(RegionBase, UpdateSchema):
    """
    Attributes to receive via API on update of a region.
    """

    name: str | None = Field(
        default=None,
        description="Unique name of the region.",
        examples=["germany"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class RegionSchema(RegionBase, ReturnSchema):
    """
    Attributes to return via API for a region.
    """

    id: int
    dataset: DatasetSchema
