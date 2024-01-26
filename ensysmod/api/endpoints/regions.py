from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud
from ensysmod.api import deps, permissions
from ensysmod.model import User
from ensysmod.schemas import RegionCreate, RegionSchema, RegionUpdate

router = APIRouter()


@router.get("/{region_id}", response_model=RegionSchema)
def get_region(
    region_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a region by its id.
    """
    region = crud.region.get(db, region_id)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {region_id} not found!")

    permissions.check_usage_permission(db=db, user=current_user, dataset_id=region.ref_dataset)

    return region


@router.get("/", response_model=list[RegionSchema])
def get_region_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all regions of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.region.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=RegionSchema, responses={409: {"description": "Region with same name already exists."}})
def create_region(
    request: RegionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new region.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.region.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Region {request.name} already for dataset {request.ref_dataset} exists!")

    return crud.region.create(db=db, obj_in=request)


@router.put("/{region_id}", response_model=RegionSchema)
def update_region(
    region_id: int,
    request: RegionUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a region.
    """
    region = crud.region.get(db=db, id=region_id)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {region_id} not found!")
    permissions.check_modification_permission(db, user=current_user, dataset_id=region.ref_dataset)
    return crud.region.update(db=db, db_obj=region, obj_in=request)


@router.delete("/{region_id}", response_model=RegionSchema)
def remove_region(
    region_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a region.
    """
    region = crud.region.get(db=db, id=region_id)
    if region is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Region {region_id} not found!")
    permissions.check_modification_permission(db, user=current_user, dataset_id=region.ref_dataset)
    return crud.region.remove(db=db, id=region_id)
