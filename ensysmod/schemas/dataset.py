from typing import Optional

from pydantic import BaseModel


class DatasetBase(BaseModel):
    """
    Shared properties for a dataset. Used as a base class for all schemas.
    """
    name: str
    description: Optional[str] = None


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
