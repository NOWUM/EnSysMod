from pydantic import Field

from ensysmod.schemas.base_schema import MAX_DESC_LENGTH, MAX_STR_LENGTH, MIN_STR_LENGTH, BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.user import User


class DatasetBase(BaseSchema):
    """
    Shared attributes for a dataset. Used as a base class for all schemas.
    """

    name: str = Field(
        default=...,
        description="Unique name of the dataset. Can be used to identify the dataset.",
        examples=["2050 Worldwide"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    description: str | None = Field(
        default=None,
        description="Description of the dataset. Can be used for a detailed description about the dataset and the modelled data.",
        examples=["Modeling year 2050 with all countries"],
        max_length=MAX_DESC_LENGTH,
    )
    hours_per_time_step: int | None = Field(
        default=1,
        description="Hours per time step in the dataset. Use 1 for hourly data, 24 for daily data. It is needed to calculate annual costs.",
        examples=[1],
        gt=0,
    )
    number_of_time_steps: int | None = Field(
        default=8760,
        description="Number of time steps in the dataset. All provided time series must have the same length.",
        examples=[8760],
        gt=0,
    )
    cost_unit: str | None = Field(
        default="1e9 €",
        description="Cost unit for the whole dataset. All provided costs must be in this unit.",
        examples=["1e9 €"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )
    length_unit: str | None = Field(
        default="km",
        description="Length unit for the whole dataset. All provided distances must be in this unit.",
        examples=["km"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class DatasetCreate(DatasetBase, CreateSchema):
    """
    Attributes to receive via API on creation of a dataset.
    """

    ref_user: int | None = Field(
        default=None,
        description="User ID of the creator. If not provided, the current user is used.",
        gt=0,
    )


class DatasetUpdate(DatasetBase, UpdateSchema):
    """
    Attributes to receive via API on update of a dataset.
    """

    name: str | None = Field(
        default=None,
        description="Unique name of the dataset. Can be used to identify the dataset.",
        examples=["2050 Worldwide"],
        min_length=MIN_STR_LENGTH,
        max_length=MAX_STR_LENGTH,
    )


class Dataset(DatasetBase, ReturnSchema):
    """
    Attributes to return via API for a dataset.
    """

    id: int = Field(default=..., description="The unique ID of the dataset.")
    user: User = Field(default=..., description="User that created the dataset.")
