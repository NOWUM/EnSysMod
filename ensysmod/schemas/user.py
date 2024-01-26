from pydantic import Field

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema


class UserBase(BaseSchema):
    """
    Shared attributes for a User. Used as a base class for all schemas.
    """


class UserCreate(UserBase, CreateSchema):
    """
    Attributes to receive via API on creation of a User.
    """

    username: str
    password: str


class UserUpdate(UserBase, UpdateSchema):
    """
    Attributes to receive via API on update of a User.
    """

    username: str | None = None
    password: str | None = None


class UserSchema(UserBase, ReturnSchema):
    """
    Attributes to return via API for a User.
    """

    id: int
    username: str
    hashed_password: str = Field(exclude=True)
