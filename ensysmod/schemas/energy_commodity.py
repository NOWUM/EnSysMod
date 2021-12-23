from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.schemas import Dataset


class EnergyCommodityBase(BaseModel):
    """
    Shared properties for an energy commodity. Used as a base class for all schemas.
    """
    name: str = Field(..., description="Name of the energy commodity", example="Electricity")
    unit: str = Field(..., description="Unit of the energy commodity", example="GW")
    description: Optional[str] = Field(None, description="Description of the energy commodity", example="Electricity")


class EnergyCommodityCreate(EnergyCommodityBase):
    """
    Properties to receive via API on creation of an energy commodity.
    """
    ref_dataset: int = Field(..., description="Reference to the dataset", example=1)


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
