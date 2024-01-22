from pydantic import Field, field_validator

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.user import User
from ensysmod.utils import validators


class DatasetBase(BaseSchema):
    """
    Shared attributes for a dataset. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="Unique name of the dataset. Can be used to identify the dataset.",
        examples=["2050 Worldwide"],
    )
    description: str | None = Field(
        default=None,
        description="Description of the dataset. Can be used for a detailed description about the dataset and the modelled data.",
        examples=["Modeling year 2050 with all countries"],
    )
    hours_per_time_step: int | None = Field(
        default=None,
        description="Hours per time step in the dataset. Use 1 for hourly data, 24 for daily data. It is needed to calculate annual costs.",
        examples=[1],
    )
    number_of_time_steps: int | None = Field(
        default=None,
        description="Number of time steps in the dataset. All provided time series must have the same length.",
        examples=[8760],
    )
    cost_unit: str | None = Field(
        default=None,
        description="Cost unit for the whole dataset. All provided costs must be in this unit.",
        examples=["1e9 €"],
    )
    length_unit: str | None = Field(
        default=None,
        description="Length unit for the whole dataset. All provided distances must be in this unit.",
        examples=["km"],
    )

    # validators
    _valid_name = field_validator("name")(validators.validate_name)
    _valid_description = field_validator("description")(validators.validate_description)


class DatasetCreate(DatasetBase, CreateSchema):
    """
    Attributes to receive via API on creation of a dataset.
    """

    ref_user: int | None = Field(default=None, description="User ID of the creator. If not provided, the current user is used.")


class DatasetUpdate(DatasetBase, UpdateSchema):
    """
    Attributes to receive via API on update of a dataset.
    """

    name: str | None = Field(default=None, description="New Name of the dataset.", examples=["2051 Worldwide"])


class Dataset(DatasetBase, ReturnSchema):
    """
    Attributes to return via API for a dataset.
    """

    id: int = Field(default=..., description="The unique ID of the dataset.")
    user: User = Field(default=..., description="User that created the dataset.")
