from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConsumptionBase(BaseModel):
    year: Optional[int] = None
    quantity: Optional[int] = None


# Properties to receive via API on creation
class ConsumptionCreate(ConsumptionBase):
    year: int
    quantity: int
    region: str
    source: str
    sink: str


# Properties to receive via API on update
class ConsumptionUpdate(ConsumptionBase):
    region: Optional[str] = None
    source: Optional[str] = None
    sink: Optional[str] = None


class ConsumptionInDBBase(ConsumptionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Consumption(ConsumptionInDBBase):
    pass


# Additional properties stored in DB
class ConsumptionInDB(ConsumptionInDBBase):
    region: Optional[int] = None
    source: Optional[int] = None
    sink: Optional[int] = None
