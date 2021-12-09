from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Dataset])
def all_datasets(db: Session = Depends(deps.get_db),
                 current: model.User = Depends(deps.get_current_user),
                 skip: int = 0,
                 limit: int = 100) -> List[schemas.Dataset]:
    """
    Retrieve all datasets.
    """
    return crud.dataset.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{dataset_id}", response_model=schemas.Dataset)
def get_dataset(dataset_id: int,
                db: Session = Depends(deps.get_db),
                current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a dataset.
    """
    # TODO Check if user has permission for dataset
    return crud.dataset.get(db, dataset_id)


@router.post("/", response_model=schemas.Dataset,
             responses={409: {"description": "Dataset with same name already exists."}})
def create_dataset(request: schemas.DatasetCreate,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Create a new dataset.
    """
    # TODO Check if user has permission for dataset
    existing_ds = crud.dataset.get_by_name(db=db, name=request.name)
    if existing_ds is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Dataset {request.name} already exists!")

    return crud.dataset.create(db=db, obj_in=request)


@router.put("/{dataset_id}", response_model=schemas.Dataset)
def update_dataset(dataset_id: int,
                   request: schemas.DatasetUpdate,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Update a dataset.
    """
    # TODO Check if user has permission for dataset
    dataset = crud.dataset.get(db=db, id=dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {dataset_id} not found!")
    return crud.dataset.update(db=db, db_obj=dataset, obj_in=request)


@router.delete("/{dataset_id}", response_model=schemas.Dataset)
def remove_dataset(dataset_id: int,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Delete a dataset.
    """
    # TODO Check if user has permission for dataset
    # TODO remove all components, commodities, regions, etc.
    return crud.dataset.remove(db=db, id=dataset_id)
