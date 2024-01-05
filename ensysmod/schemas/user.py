from pydantic import BaseModel


# Shared attributes
class UserBase(BaseModel):
    username: str | None = None


# Attributes to receive via API on creation
class UserCreate(UserBase):
    username: str
    password: str


# Attributes to receive via API on update
class UserUpdate(UserBase):
    password: str | None = None


class UserInDBBase(UserBase):
    id: int | None = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
