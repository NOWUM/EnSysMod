from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.util import validators


class DatasetBase(BaseModel):
    """
    Shared properties for a dataset. Used as a base class for all schemas.
    """
    name: str
    description: Optional[str] = None

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class DatasetCreate(DatasetBase):
    """
    Properties to receive via API on creation of a dataset.
    """
    pass


class DatasetUpdate(DatasetBase):
    """
    Properties to receive via API on update of a dataset.
    """
    name: Optional[str] = None


class Dataset(DatasetBase):
    """
    Properties to return via API for a dataset.
    """
    id: int

    class Config:
        orm_mode = True
