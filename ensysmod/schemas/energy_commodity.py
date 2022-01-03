from typing import Optional

from pydantic import BaseModel, validator

from ensysmod.schemas import Dataset
from ensysmod.util import validators


class EnergyCommodityBase(BaseModel):
    """
    Shared properties for an energy commodity. Used as a base class for all schemas.
    """
    name: str
    unit: str
    description: Optional[str] = None

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_unit = validator("unit", allow_reuse=True)(validators.validate_unit)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyCommodityCreate(EnergyCommodityBase):
    """
    Properties to receive via API on creation of an energy commodity.
    """
    ref_dataset: int

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset)

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
