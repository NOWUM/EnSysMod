from typing import Optional

from pydantic import BaseModel


# Shared properties
class EnergySinkBase(BaseModel):
    name: Optional[str] = None


# Properties to receive via API on creation
class EnergySinkCreate(EnergySinkBase):
    name: str
    description: Optional[str] = None


# Properties to receive via API on update
class EnergySinkUpdate(EnergySinkBase):
    name: Optional[str] = None
    description: Optional[str] = None


class EnergySinkInDBBase(EnergySinkBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class EnergySink(EnergySinkInDBBase):
    pass


# Additional properties stored in DB
class EnergySinkInDB(EnergySinkInDBBase):
    description: Optional[str] = None
