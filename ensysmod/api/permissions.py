from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.schemas import User


def check_modification_permission(db: Session, user: User, dataset_id: int):
    """Check if the user has permission to modify the dataset.

    Args:
        db: The database session.
        user: The user.
        dataset_id: The dataset id.
    """
    if not crud.dataset_permission.is_modification_allowed(db, dataset_id=dataset_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to modify this dataset!")


def check_usage_permission(db: Session, user: User, dataset_id: int):
    """Check if the user has permission to use the dataset.

    Args:
        db: The database session.
        user: The user.
        dataset_id: The dataset id.
    """
    if not crud.dataset_permission.is_usage_allowed(db, dataset_id=dataset_id, user_id=user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to use this dataset!")
