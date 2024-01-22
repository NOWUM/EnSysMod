from pydantic import Field, field_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import Dataset
from ensysmod.utils import validators


class EnergyCommodityBase(BaseSchema):
    """
    Shared attributes for an energy commodity. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="The unique name of the energy commodity inside this dataset. It is needed to add energy components of this specific commodity.",
        examples=["Electricity"],
    )
    unit: str = Field(
        default=...,
        description="Unit of the energy commodity. Every provided data for this commodity must be in this unit.",
        examples=["GW"],
    )
    description: str | None = Field(
        default=None,
        description="Description of the energy commodity. Can be used as detailed description of the energy commodity.",
        examples=["Electricity"],
    )

    # validators
    _valid_name = field_validator("name")(validators.validate_name)
    _valid_unit = field_validator("unit")(validators.validate_unit)
    _valid_description = field_validator("description")(validators.validate_description)


class EnergyCommodityCreate(EnergyCommodityBase, CreateSchema):
    """
    Attributes to receive via API on creation of an energy commodity.
    """

    ref_dataset: int = Field(default=..., description="Reference to the dataset where that energy commodity belongs to.", examples=[1])

    # validators
    _valid_ref_dataset = field_validator("ref_dataset")(validators.validate_ref_dataset_required)


class EnergyCommodityUpdate(EnergyCommodityBase, UpdateSchema):
    """
    Attributes to receive via API on update of an energy commodity.
    """

    name: str | None = Field(default=None, description="New Name of the energy commodity.", examples=["Electricity"])
    unit: str | None = Field(default=None, description="New Unit of the energy commodity.", examples=["GW"])


class EnergyCommodity(EnergyCommodityBase, ReturnSchema):
    """
    Attributes to return via API for an energy commodity.
    """

    id: int = Field(default=..., description="The unique ID of the energy commodity.")
    dataset: Dataset = Field(default=..., description="Dataset object where the energy commodity belongs to.")
