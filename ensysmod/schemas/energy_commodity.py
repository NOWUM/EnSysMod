from pydantic import Field

from ensysmod.schemas.base_schema import MAX_DESC_LENGTH, MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import DatasetSchema


class EnergyCommodityBase(BaseSchema):
    """
    Shared attributes for an energy commodity. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="The unique name of the energy commodity inside this dataset. It is needed to add energy components of this specific commodity.",
        examples=["Electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    description: str | None = Field(
        default=None,
        description="Description of the energy commodity. Can be used as detailed description of the energy commodity.",
        examples=["Electricity"],
        max_length=MAX_DESC_LENGTH,
    )
    unit: str = Field(
        default=...,
        description="Unit of the energy commodity. Every provided data for this commodity must be in this unit.",
        examples=["GW"],
        max_length=MAX_STR_LENGTH,
    )


class EnergyCommodityCreate(EnergyCommodityBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy commodity.
    """

    ref_dataset: int = Field(
        default=...,
        description="Reference to the dataset where that energy commodity belongs to.",
        examples=[1],
        gt=0,
    )


class EnergyCommodityUpdate(EnergyCommodityBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy commodity.
    """

    name: str | None = Field(
        default=None,
        description="The unique name of the energy commodity inside this dataset. It is needed to add energy components of this specific commodity.",
        examples=["Electricity"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    unit: str | None = Field(
        default=None,
        description="Unit of the energy commodity. Every provided data for this commodity must be in this unit.",
        examples=["GW"],
        max_length=MAX_STR_LENGTH,
    )


class EnergyCommoditySchema(EnergyCommodityBase, ReturnSchema):
    """
    Attributes to return via API for an energy commodity.
    """

    id: int = Field(default=..., description="The unique ID of the energy commodity.")
    dataset: DatasetSchema = Field(default=..., description="Dataset object where the energy commodity belongs to.")
