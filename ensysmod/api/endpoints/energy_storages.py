from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=List[schemas.EnergyStorage])
def all_energy_storages(db: Session = Depends(deps.get_db),
                        current: model.User = Depends(deps.get_current_user),
                        skip: int = 0,
                        limit: int = 100) -> List[schemas.EnergyStorage]:
    """
    Retrieve all energy storages.
    """
    return crud.energy_storage.get_multi(db, skip, limit)


@router.post("/", response_model=schemas.EnergyStorage,
             responses={409: {"description": "EnergyStorage with same name already exists."}})
def create_storage(request: schemas.EnergyStorageCreate,
                   db: Session = Depends(deps.get_db),
                   current: model.User = Depends(deps.get_current_user)):
    """
    Create a new energy storage.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    existing = crud.energy_storage.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"EnergyStorage {request.name} already for dataset {request.ref_dataset} exists!")

    # Check if energy commodity exists
    commodity = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset,
                                                              name=request.commodity)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"EnergyCommodity {request.commodity} in dataset {request.ref_dataset} not found!")

    return crud.energy_storage.create(db=db, obj_in=request)
