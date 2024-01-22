from pydantic import Field, field_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import Dataset
from ensysmod.utils import validators


class RegionBase(BaseSchema):
    """
    Shared attributes for a region. Used as a base class for all schemas.
    """

    name: str = Field(default=..., description="Unique name of the region.", examples=["germany"])

    # validators
    _valid_name = field_validator("name")(validators.validate_name)


class RegionCreate(RegionBase, CreateSchema):
    """
    Attributes to receive via API on creation of a region.
    """

    ref_dataset: int = Field(default=..., description="ID of the dataset to use as reference.", examples=[1])

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_required)


class RegionUpdate(RegionBase, UpdateSchema):
    """
    Attributes to receive via API on update of a region.
    """

    name: str | None = Field(default=None, description="New name of the region", examples=["germany"])


class Region(RegionBase, ReturnSchema):
    """
    Attributes to return via API for a region.
    """

    id: int
    dataset: Dataset
