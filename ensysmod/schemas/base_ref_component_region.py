from pydantic import Field, field_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import Dataset
from ensysmod.schemas.energy_component import EnergyComponent
from ensysmod.schemas.region import Region
from ensysmod.utils import validators


class RefCRBaseBase(BaseSchema):
    """
    Shared attributes for an object with a reference to a component and region. Used as a base class for all schemas.
    """


class RefCRBaseCreate(CreateSchema):
    """
    Attributes to receive via API on creation of an object with a reference to a component and region.
    """

    ref_dataset: int = Field(default=..., description="The ID of the referenced dataset. Current dataset is used as default.")
    component: str = Field(default=..., description="The name of the component.", examples=["heat_pump"])
    region: str = Field(default=..., description="The name of the region.", examples=["germany"])
    region_to: str | None = Field(default=None, description="Optional region to name, if needed.", examples=["france"])

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_required)


class RefCRBaseUpdate(UpdateSchema):
    """
    Attributes to receive via API on update of an object with a reference to a component and region.
    """


class RefCRBase(ReturnSchema):
    """
    Attributes to return via API for an object with a reference to a component and region.
    """

    id: int
    dataset: Dataset
    component: EnergyComponent
    region: Region
    region_to: Region | None = None
