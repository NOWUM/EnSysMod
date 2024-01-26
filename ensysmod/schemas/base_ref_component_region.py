from pydantic import Field

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import DatasetSchema
from ensysmod.schemas.energy_component import EnergyComponentSchema
from ensysmod.schemas.region import RegionSchema


class RefCRBaseBase(BaseSchema):
    """
    Shared attributes for an object with a reference to a component and region. Used as a base class for all schemas.
    """


class RefCRBaseCreate(CreateSchema):
    """
    Attributes to receive via API on creation of an object with a reference to a component and region.
    """

    ref_dataset: int = Field(
        default=...,
        description="The ID of the referenced dataset. Current dataset is used as default.",
        gt=0,
    )
    component: str = Field(
        default=...,
        description="The name of the component.",
        examples=["heat_pump"],
    )
    region: str = Field(
        default=...,
        description="The name of the region.",
        examples=["germany"],
    )
    region_to: str | None = Field(
        default=None,
        description="Optional region to name, if needed.",
        examples=["france"],
    )


class RefCRBaseUpdate(UpdateSchema):
    """
    Attributes to receive via API on update of an object with a reference to a component and region.
    """


class RefCRBase(ReturnSchema):
    """
    Attributes to return via API for an object with a reference to a component and region.
    """

    id: int
    dataset: DatasetSchema
    component: EnergyComponentSchema
    region: RegionSchema
    region_to: RegionSchema | None = None
