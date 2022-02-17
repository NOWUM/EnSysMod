from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ensysmod import schemas, model, crud
from ensysmod.api import deps, permissions

router = APIRouter()


@router.get("/", response_model=List[schemas.EnergyCommodity])
def all_commodities(db: Session = Depends(deps.get_db),
                    current: model.User = Depends(deps.get_current_user),
                    skip: int = 0,
                    limit: int = 100,
                    dataset: Union[None, int] = None) -> List[schemas.EnergyCommodity]:
    """
    Retrieve all energy commodities.
    """
    if dataset is None:
        return crud.energy_commodity.get_multi(db, skip=skip, limit=limit)
    else:
        return crud.energy_commodity.get_multi_by_dataset(db, dataset_id=dataset, skip=skip, limit=limit)


@router.get("/{commodity_id}", response_model=schemas.EnergyCommodity)
def get_commodity(commodity_id: int,
                  db: Session = Depends(deps.get_db),
                  current: model.User = Depends(deps.get_current_user)):
    """
    Retrieve a energy commodity.
    """
    return crud.energy_commodity.get(db, commodity_id)


@router.post("/", response_model=schemas.EnergyCommodity,
             responses={409: {"description": "EnergyCommodity with same name already exists."}})
def create_commodity(request: schemas.EnergyCommodityCreate,
                     db: Session = Depends(deps.get_db),
                     current: model.User = Depends(deps.get_current_user)):
    """
    Create a new energy commodity.
    """
    dataset = crud.dataset.get(db=db, id=request.ref_dataset)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Dataset {request.ref_dataset} not found!")

    permissions.check_modification_permission(db, user=current, dataset_id=request.ref_dataset)

    existing = crud.energy_commodity.get_by_dataset_and_name(db=db, dataset_id=request.ref_dataset, name=request.name)
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"EnergyCommodity {request.name} already for dataset {request.ref_dataset} exists!")

    return crud.energy_commodity.create(db=db, obj_in=request)


@router.put("/{commodity_id}", response_model=schemas.EnergyCommodity)
def update_commodity(commodity_id: int,
                     request: schemas.EnergyCommodityUpdate,
                     db: Session = Depends(deps.get_db),
                     current: model.User = Depends(deps.get_current_user)):
    """
    Update a energy commodity.
    """
    commodity = crud.energy_commodity.get(db=db, id=commodity_id)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyCommodity {commodity_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=commodity.ref_dataset)
    return crud.energy_commodity.update(db=db, db_obj=commodity, obj_in=request)


@router.delete("/{commodity_id}", response_model=schemas.EnergyCommodity)
def remove_commodity(commodity_id: int,
                     db: Session = Depends(deps.get_db),
                     current: model.User = Depends(deps.get_current_user)):
    """
    Delete a energy commodity.
    """
    commodity = crud.energy_commodity.get(db=db, id=commodity_id)
    if commodity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"EnergyCommodity {commodity_id} not found!")
    permissions.check_modification_permission(db, user=current, dataset_id=commodity.ref_dataset)
    return crud.energy_commodity.remove(db=db, id=commodity_id)
