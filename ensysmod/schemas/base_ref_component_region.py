from pydantic import Field

from ensysmod.schemas.base_schema import MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import DatasetSchema
from ensysmod.schemas.energy_component import EnergyComponentSchema
from ensysmod.schemas.region import RegionSchema


class RefCRBaseBase(BaseSchema):
    """
    Shared attributes for an object with a reference to a component and region. Used as a base class for all schemas.
    """


class RefCRBaseCreate(RefCRBaseBase, CreateSchema):
    """
    Attributes to receive via API on creation of an object with a reference to a component and region.
    """

    ref_dataset: int = Field(
        default=...,
        description="The ID of the referenced dataset. Current dataset is used as default.",
        examples=[1],
        gt=0,
    )
    component_name: str = Field(
        default=...,
        description="The name of the component.",
        examples=["heat_pump"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    region_name: str = Field(
        default=...,
        description="The name of the region.",
        examples=["germany"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    region_to_name: str | None = Field(
        default=None,
        description="Optional region to name, if needed.",
        examples=["france"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class RefCRBaseUpdate(RefCRBaseBase, UpdateSchema):
    """
    Attributes to receive via API on update of an object with a reference to a component and region.
    """


class RefCRBase(RefCRBaseBase, ReturnSchema):
    """
    Attributes to return via API for an object with a reference to a component and region.
    """

    id: int
    dataset: DatasetSchema
    component: EnergyComponentSchema
    region: RegionSchema
    region_to: RegionSchema | None
