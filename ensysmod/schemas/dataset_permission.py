from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.schemas.user import User
from ensysmod.schemas.dataset import Dataset


class DatasetPermissionBase(BaseModel):
    """
    Shared attributes for a DatasetPermission. Used as a base class for all schemas.
    """
    allow_usage: bool = Field(True, description="Whether the user is allowed to use the dataset.")
    allow_modification: bool = Field(True, description="Whether the user is allowed to modify the dataset.")
    allow_permission_grant: bool = Field(True, description="Whether the user is allowed to grant permissions.")
    allow_permission_revoke: bool = Field(True, description="Whether the user is allowed to revoke permissions.")


class DatasetPermissionCreate(DatasetPermissionBase):
    """
    Attributes to receive via API on creation of a DatasetPermission.
    """
    ref_dataset: Optional[int] = Field(None, description="The ID of the dataset. "
                                                         "You must have access to grant permissions to this dataset.")
    ref_user: Optional[int] = Field(None, description="The ID of the user that receive the permissions.")


class DatasetPermissionUpdate(DatasetPermissionBase):
    """
    Attributes to receive via API on update of a DatasetPermission.
    """
    pass


class DatasetPermission(DatasetPermissionBase):
    """
    Attributes to return via API for a DatasetPermission.
    """
    id: int = Field(..., description="The unique ID of the DatasetPermission.")
    dataset: Dataset = Field(..., description="The dataset that the permissions are granted to.")
    user: User = Field(..., description="The user that the permissions are granted to.")

    class Config:
        orm_mode = True
