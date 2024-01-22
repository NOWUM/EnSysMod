from pydantic import Field

from ensysmod.schemas.base_schema import BaseSchema, CreateSchema, ReturnSchema, UpdateSchema
from ensysmod.schemas.dataset import Dataset
from ensysmod.schemas.user import User


class DatasetPermissionBase(BaseSchema):
    """
    Shared attributes for a DatasetPermission. Used as a base class for all schemas.
    """

    allow_usage: bool = Field(default=True, description="Whether the user is allowed to use the dataset.")
    allow_modification: bool = Field(default=True, description="Whether the user is allowed to modify the dataset.")
    allow_permission_grant: bool = Field(default=True, description="Whether the user is allowed to grant permissions.")
    allow_permission_revoke: bool = Field(default=True, description="Whether the user is allowed to revoke permissions.")


class DatasetPermissionCreate(DatasetPermissionBase, CreateSchema):
    """
    Attributes to receive via API on creation of a DatasetPermission.
    """

    ref_dataset: int | None = Field(default=None, description="The ID of the dataset. You must have access to grant permissions to this dataset.")
    ref_user: int | None = Field(default=None, description="The ID of the user that receive the permissions.")


class DatasetPermissionUpdate(DatasetPermissionBase, UpdateSchema):
    """
    Attributes to receive via API on update of a DatasetPermission.
    """


class DatasetPermission(DatasetPermissionBase, ReturnSchema):
    """
    Attributes to return via API for a DatasetPermission.
    """

    id: int = Field(default=..., description="The unique ID of the DatasetPermission.")
    dataset: Dataset = Field(default=..., description="The dataset that the permissions are granted to.")
    user: User = Field(default=..., description="The user that the permissions are granted to.")
