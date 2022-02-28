from typing import Optional

from pydantic import BaseModel, Field, validator

from ensysmod.schemas import Dataset
from ensysmod.util import validators


class EnergyCommodityBase(BaseModel):
    """
    Shared attributes for an energy commodity. Used as a base class for all schemas.
    """
    name: str = Field(...,
                      description="The unique name of the energy commodity inside this dataset. "
                                  "It is needed to add energy components of this specific commodity.",
                      example="Electricity")
    unit: str = Field(...,
                      description="Unit of the energy commodity. "
                                  "Every provided data for this commodity must be in this unit.",
                      example="GW")
    description: Optional[str] = Field(None,
                                       description="Description of the energy commodity."
                                                   "Can be used as detailed description of the energy commodity.",
                                       example="Electricity")

    # validators
    _valid_name = validator("name", allow_reuse=True)(validators.validate_name)
    _valid_unit = validator("unit", allow_reuse=True)(validators.validate_unit)
    _valid_description = validator("description", allow_reuse=True)(validators.validate_description)


class EnergyCommodityCreate(EnergyCommodityBase):
    """
    Attributes to receive via API on creation of an energy commodity.
    """
    ref_dataset: int = Field(...,
                             description="Reference to the dataset where that energy commodity belongs to.",
                             example=1)

    # validators
    _valid_ref_dataset = validator("ref_dataset", allow_reuse=True)(validators.validate_ref_dataset_required)


class EnergyCommodityUpdate(EnergyCommodityBase):
    """
    Attributes to receive via API on update of an energy commodity.
    """
    name: Optional[str] = Field(None, description="New Name of the energy commodity.", example="Electricity")
    unit: Optional[str] = Field(None, description="New Unit of the energy commodity.", example="GW")


class EnergyCommodity(EnergyCommodityBase):
    """
    Attributes to return via API for an energy commodity.
    """
    id: int = Field(..., description="The unique ID of the energy commodity.")
    dataset: Dataset = Field(..., description="Dataset object where the energy commodity belongs to.")

    class Config:
        orm_mode = True
