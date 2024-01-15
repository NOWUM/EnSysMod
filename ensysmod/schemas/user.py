from pydantic import BaseModel


# Shared attributes
class UserBase(BaseModel):
    """
    Shared attributes for a User. Used as a base class for all schemas.
    """


class UserCreate(UserBase):
    """
    Attributes to receive via API on creation of a User.
    """

    username: str
    password: str


class UserUpdate(UserBase):
    """
    Attributes to receive via API on update of a User.
    """

    username: str | None = None
    password: str | None = None


class User(UserBase):
    """
    Attributes to return via API for a User.
    """

    id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True
