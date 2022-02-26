from typing import Optional

from pydantic import BaseModel, Field, validator

from ensysmod.schemas import Dataset
from ensysmod.util import validators


class EnergyCommodityBase(BaseModel):
    """
    Shared properties for an energy commodity. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the energy commodity", example="Electricity")
    unit: str = Field(..., description="Unit of the energy commodity", example="GW")
    description: Optional[str] = Field(None, description="Description of the energy commodity", example="Electricity")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_unit = validator("unit", allow_reuse=True)(validators.validate_unit)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyCommodityCreate(EnergyCommodityBase):
    """
    Properties to receive via API on creation of an energy commodity.
    """
    ref_dataset: int = Field(..., description="Reference to the dataset", example=1)

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyCommodityUpdate(EnergyCommodityBase):
    """
    Properties to receive via API on update of an energy commodity.
    """
    name: Optional[str] = Field(None, description="New Name of the energy commodity", example="Electricity")
    unit: Optional[str] = Field(None, description="New Unit of the energy commodity", example="GW")


class EnergyCommodity(EnergyCommodityBase):
    """
    Properties to return via API for an energy commodity.
    """
    id: int = Field(..., description="Id of the energy commodity")
    dataset: Dataset = Field(..., description="Dataset object where the energy commodity belongs to")

    class Config:
        orm_mode = True
