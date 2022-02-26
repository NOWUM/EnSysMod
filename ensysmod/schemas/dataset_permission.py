from typing import Optional

from pydantic import BaseModel, Field

from ensysmod.schemas.user import User
from ensysmod.schemas.dataset import Dataset


class DatasetPermissionBase(BaseModel):
    """
    Shared properties for a DatasetPermission. Used as a base class for all schemas.
    """
    allow_usage: bool = Field(True, description="Whether the user is allowed to use the dataset.")
    allow_modification: bool = Field(True, description="Whether the user is allowed to modify the dataset.")
    allow_permission_grant: bool = Field(True, description="Whether the user is allowed to grant permissions.")
    allow_permission_revoke: bool = Field(True, description="Whether the user is allowed to revoke permissions.")


class DatasetPermissionCreate(DatasetPermissionBase):
    """
    Properties to receive via API on creation of a DatasetPermission.
    """
    ref_dataset: Optional[int] = None
    ref_user: Optional[int] = None


class DatasetPermissionUpdate(DatasetPermissionBase):
    """
    Properties to receive via API on update of a DatasetPermission.
    """
    pass


class DatasetPermission(DatasetPermissionBase):
    """
    Properties to return via API for a DatasetPermission.
    """
    id: int
    dataset: Dataset
    user: User

    class Config:
        orm_mode = True
