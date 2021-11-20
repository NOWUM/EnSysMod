from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConsumptionBase(BaseModel):
    year: Optional[int] = None
    quantity: Optional[int] = None


# Properties to receive via API on creation
class consumptionCreate(consumptionBase):
    year: int
    quantity: int
    region: str
    source: str
    sink: str


# Properties to receive via API on update
class consumptionUpdate(consumptionBase):
    year: Optional[id] = None
    quantity: Optional[id] = None
    region: Optional[id] = None
    source: Optional[id] = None
    sink: Optional[id] = None


class consumptionInDBBase(consumptionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class consumption(consumptionInDBBase):
    pass


# Additional properties stored in DB
class consumptionInDB(consumptionInDBBase):
    region: Optional[str] = None
    source: Optional[str] = None
    sink: Optional[str] = None
