from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Shared attributes for an object. Used as a base class for all schemas.
    """


class CreateSchema(BaseSchema):
    """
    Attributes to receive via API on creation of an object.
    """


class UpdateSchema(BaseSchema):
    """
    Attributes to receive via API on update of an object.
    """


class ReturnSchema(BaseSchema):
    """
    Attributes to return via API for an object.
    """

    model_config = ConfigDict(from_attributes=True)
