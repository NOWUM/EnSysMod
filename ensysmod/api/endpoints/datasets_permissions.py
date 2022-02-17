from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.DatasetPermission])
def all_dataset_permission(db: Session = Depends(deps.get_db),
                           current: model.User = Depends(deps.get_current_user),
                           dataset_id: int = 0,
                           user_id: int = 0,
                           skip: int = 0,
                           limit: int = 100) -> List[schemas.DatasetPermission]:
    """
    Retrieve all dataset permissions.

    If you provide a dataset_id, only the permissions for that dataset will be returned.

    If you provide a user_id, only the permissions for that user will be returned.

    Otherwise, all of your personal permissions will be returned.
    """
    if dataset_id != 0:
        if not crud.dataset_permission.is_permission_check_allowed(db=db,
                                                                   dataset_id=dataset_id,
                                                                   user_id=current.id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You have no permission to check permissions for this dataset.")
        return crud.dataset_permission.get_by_dataset_id(db=db, dataset_id=dataset_id, skip=skip, limit=limit)

    if user_id != 0:
        if user_id != current.id:
            # TODO Add admin permission to user, that allow this function
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You have no permission to check permissions for this user.")
        return crud.dataset_permission.get_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)

    return crud.dataset_permission.get_by_user_id(db=db, user_id=current.id, skip=skip, limit=limit)


@router.get("/{permission_id}", response_model=schemas.DatasetPermission)
def get_dataset_permission(permission_id: int,
                           db: Session = Depends(deps.get_db),
                           current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a dataset-user permission.
    """
    existing_permission = crud.dataset_permission.get(db, permission_id)
    if existing_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Dataset permission not found for id {permission_id}.")

    if not crud.dataset_permission.is_permission_check_allowed(db=db,
                                                               dataset_id=existing_permission.ref_dataset,
                                                               user_id=current.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have no permission to check permissions for this dataset.")

    return crud.dataset_permission.get(db, permission_id)


@router.post("/", response_model=schemas.DatasetPermission,
             responses={409: {"description": "Dataset permission for same user already exists."}})
def create_dataset_permission(request: schemas.DatasetPermissionCreate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Create a new dataset_permission.
    """
    if not crud.dataset_permission.is_permission_grant_allowed(db=db,
                                                               dataset_id=request.ref_dataset,
                                                               user_id=current.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have no permission to grant permissions to other users for this dataset.")

    permission = crud.dataset_permission.get_by_user_id(db=db, user_id=request.ref_user, dataset_id=request.ref_dataset)
    if permission is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Dataset permission for same user already exists.")

    return crud.dataset_permission.create(db=db, obj_in=request)


@router.put("/{permission_id}", response_model=schemas.DatasetPermission)
def update_dataset_permission(permission_id: int,
                              request: schemas.DatasetPermissionUpdate,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Update a dataset-user permission.

    You can not edit your own permissions.

    For editing other permissions, you need grant and revoke permissions.
    (Might change in future.)
    """
    existing_permission = crud.dataset_permission.get(db, permission_id)
    if existing_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Dataset permission not found for id {permission_id}.")

    if existing_permission.ref_user == current.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You cannot edit your own dataset permissions.")

    if not crud.dataset_permission.is_permission_grant_allowed(db=db,
                                                               dataset_id=existing_permission.ref_dataset,
                                                               user_id=current.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have no permission to grant permissions to other users for this dataset.")

    if not crud.dataset_permission.is_permission_revoke_allowed(db=db,
                                                                dataset_id=existing_permission.ref_dataset,
                                                                user_id=current.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have no permission to revoke permissions from other users for this dataset.")

    return crud.dataset_permission.update(db=db, obj_in=request, permission_id=permission_id)


@router.delete("/{permission_id}", response_model=schemas.DatasetPermission)
def remove_dataset_permission(permission_id: int,
                              db: Session = Depends(deps.get_db),
                              current: model.User = Depends(deps.get_current_user)):
    """
    Delete a dataset-user permission.
    """
    existing_permission = crud.dataset_permission.get(db, permission_id)
    if existing_permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Dataset permission not found for id {permission_id}.")

    if existing_permission.ref_user == current.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You cannot edit your own dataset permissions.")

    if not crud.dataset_permission.is_permission_revoke_allowed(db=db,
                                                                dataset_id=existing_permission.ref_dataset,
                                                                user_id=current.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You have no permission to revoke permissions from other users for this dataset.")

    return crud.dataset_permission.remove(db=db, id=permission_id)
