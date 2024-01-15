from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import crud, model, schemas
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=list[schemas.EnergyStorage])
def get_energy_storage_by_dataset(
    dataset_id: int,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Get all energy storages of a dataset.
    """
    permissions.check_usage_permission(db=db, user=current_user, dataset_id=dataset_id)
    return crud.energy_storage.get_multi_by_dataset(db=db, skip=skip, limit=limit, dataset_id=dataset_id)


@router.post("/", response_model=schemas.EnergyStorage, responses={409: {"description": "EnergyStorage with same name already exists."}})
def create_storage(
    request: schemas.EnergyStorageCreate,
    db: Session = Depends(deps.get_db),
    current_user: model.User = Depends(deps.get_current_user),
):
    """
    Create a new energy storage.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current_user, dataset_id=request.ref_dataset)

    existing = crud.energy_storage.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"EnergyStorage {request.name} already for dataset {request.ref_dataset} exists!",
        )

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.commodity)
    if commodity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"EnergyCommodity {request.commodity} in dataset {request.ref_dataset} not found!",
        )

    return crud.energy_storage.create(db=db, obj_in=request)
