from pydantic import BaseModel, ConfigDict

MIN_STR_LENGTH = 1
MAX_STR_LENGTH = 255
MAX_DESC_LENGTH = 1024


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
