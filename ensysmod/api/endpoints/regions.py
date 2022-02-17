from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=List[schemas.Region])
def all_regions(db: Session = Depends(deps.get_db),
                current: model.User = Depends(deps.get_current_user),
                skip: int = 0,
                limit: int = 100,
                dataset: Union[None, int] = None) -> List[schemas.Region]:
    """
    Retrieve all energy regions.
    """
    if dataset is None:
        return crud.region.get_multi(db, skip=skip, limit=limit)
    else:
        return crud.region.get_multi_by_dataset(db, dataset_id=dataset, skip=skip, limit=limit)


@router.get("/{region_id}", response_model=schemas.Region)
def get_region(region_id: int,
               db: Session = Depends(deps.get_db),
               current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a region.
    """
    return crud.region.get(db, region_id)


@router.post("/", response_model=schemas.Region,
             responses={409: {"description": "Region with same name already exists."}})
def create_region(request: schemas.RegionCreate,
                  db: Session = Depends(deps.get_db),
                  current: model.User = Depends(deps.get_current_user)):
    """
    Create a new region.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    existing = crud.region.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Region {request.name} already for dataset {request.ref_dataset} exists!")

    return crud.region.create(db=db, obj_in=request)


@router.put("/{region_id}", response_model=schemas.Region)
def update_region(region_id: int,
                  request: schemas.RegionUpdate,
                  db: Session = Depends(deps.get_db),
                  current: model.User = Depends(deps.get_current_user)):
    """
    Update a region.
    """
    region = crud.region.get(db=db, id=region_id)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {region_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=region.ref_dataset)
    return crud.region.update(db=db, db_obj=region, obj_in=request)


@router.delete("/{region_id}", response_model=schemas.Region)
def remove_region(region_id: int,
                  db: Session = Depends(deps.get_db),
                  current: model.User = Depends(deps.get_current_user)):
    """
    Delete a region.
    """
    region = crud.region.get(db=db, id=region_id)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {region_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=region.ref_dataset)
    return crud.region.remove(db=db, id=region_id)
