from typing import Optional

from pydantic import BaseModel, Field


class DatasetBase(BaseModel):
    """
    Shared properties for a dataset. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the dataset", example="2050 Worldwide")
    description: Optional[str] = Field(None, description="Description of the dataset",
                                       example="Modeling year 2050 with all countries")


class DatasetCreate(DatasetBase):
    """
    Properties to receive via API on creation of a dataset.
    """
    pass


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

    class Config:
        orm_mode = True
