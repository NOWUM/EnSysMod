from typing import Optional

from pydantic import BaseModel

from ensysmod.schemas import Dataset


class EnergyCommodityBase(BaseModel):
    """
    Shared properties for an energy commodity. Used as a base class for all schemas.
    """
    name: str
    unit: str
    description: Optional[str] = None


class EnergyCommodityCreate(EnergyCommodityBase):
    """
    Properties to receive via API on creation of an energy commodity.
    """
    ref_dataset: int


class EnergyCommodityUpdate(EnergyCommodityBase):
    """
    Properties to receive via API on update of an energy commodity.
    """
    name: Optional[str] = None
    unit: Optional[str] = None


class EnergyCommodity(EnergyCommodityBase):
    """
    Properties to return via API for an energy commodity.
    """
    id: int
    dataset: Dataset

    class Config:
        orm_mode = True
