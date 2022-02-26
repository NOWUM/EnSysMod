from typing import Optional

from pydantic import BaseModel, Field, validator

from ensysmod.util import validators

from ensysmod.schemas.user import User


class DatasetBase(BaseModel):
    """
    Shared properties for a dataset. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the dataset", example="2050 Worldwide")
    description: Optional[str] = Field(None, description="Description of the dataset",
                                       example="Modeling year 2050 with all countries")
    hours_per_time_step: Optional[int] = None
    number_of_time_steps: Optional[int] = None
    cost_unit: Optional[str] = None
    length_unit: Optional[str] = None

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class DatasetCreate(DatasetBase):
    """
    Properties to receive via API on creation of a dataset.
    """
    ref_created_by: Optional[int] = None


class DatasetUpdate(DatasetBase):
    """
    Properties to receive via API on update of a dataset.
    """
    name: Optional[str] = Field(None, description="New Name of the dataset", example="2051 Worldwide")


class Dataset(DatasetBase):
    """
    Properties to return via API for a dataset.
    """
    id: int = Field(..., description="Id of the dataset", example=1)
    created_by: User

    class Config:
        orm_mode = True
