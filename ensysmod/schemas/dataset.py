from typing import Optional

from pydantic import BaseModel, Field, validator

from ensysmod.schemas.user import User
from ensysmod.util import validators


class DatasetBase(BaseModel):
    """
    Shared attributes for a dataset. Used as a base class for all schemas.
    """
    name: str = Field(...,
                      description="Unique name of the dataset. Can be used to identify the dataset.",
                      example="2050 Worldwide")

    description: Optional[str] = Field(None,
                                       description="Description of the dataset. Can be used for a detailed "
                                                   "description about the dataset and the modelled data.",
                                       example="Modeling year 2050 with all countries")
    hours_per_time_step: Optional[int] = Field(None,
                                               description="Hours per time step in the dataset. "
                                                           "Use 1 for hourly data, 24 for daily data. "
                                                           "It is needed to calculate annual costs.",
                                               example=1)
    number_of_time_steps: Optional[int] = Field(None,
                                                description="Number of time steps in the dataset."
                                                            "All provided time series must have the same length.",
                                                example=8760)
    cost_unit: Optional[str] = Field(None,
                                     description="Cost unit for the hole dataset. "
                                                 "All provided costs must be in this unit.",
                                     example="1e9 €")
    length_unit: Optional[str] = Field(None,
                                       description="Length unit for the hole dataset."
                                                   "All provided distances must be in this unit.",
                                       example="km")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class DatasetCreate(DatasetBase):
    """
    Attributes to receive via API on creation of a dataset.
    """
    ref_created_by: Optional[int] = Field(None,
                                          description="User ID of the creator. "
                                                      "If not provided, the current user is used.")


class DatasetUpdate(DatasetBase):
    """
    Attributes to receive via API on update of a dataset.
    """
    name: Optional[str] = Field(None, description="New Name of the dataset.", example="2051 Worldwide")


class Dataset(DatasetBase):
    """
    Attributes to return via API for a dataset.
    """
    id: int = Field(..., description="The unique ID of the dataset.")
    created_by: User = Field(..., description="User that created the dataset.")

    class Config:
        orm_mode = True
