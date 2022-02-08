from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas.user import User


class DatasetBase(BaseModel):
    """
    Shared properties for a dataset. Used as a base class for all schemas.
    """
    name: str
    description: Optional[str] = None
    hours_per_time_step: Optional[int] = None
    number_of_time_steps: Optional[int] = None
    cost_unit: Optional[str] = None
    length_unit: Optional[str] = None


class DatasetCreate(DatasetBase):
    """
    Properties to receive via API on creation of a dataset.
    """
    ref_created_by: Optional[int] = None


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
    created_by: User

    class Config:
        orm_mode = True
